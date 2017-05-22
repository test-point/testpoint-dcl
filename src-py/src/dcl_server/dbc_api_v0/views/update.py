from __future__ import unicode_literals
import logging

from rest_framework import generics, serializers, response, status

from dcl_server.accreditations.models import AccreditedParty
from dcl_server.dcl_audit.models import DclRecordUpdateToken
from dcl_server.backends.generic import update_dcl_record, clear_dcl_record
from dcl_server.oasis.constants import (
    OASIS_PREFIX_ABN, OASIS_PREFIX_GLN, OASIS_PREFIX_DUNS,
    OASIS_PREFIX_UNREGISTERED
)
from dcl_server.oasis.utils import get_hash

logger = logging.getLogger(__name__)


class UpdateDclRecordSerializer(serializers.Serializer):
    SUPPORTED_SCHEMES = (
        OASIS_PREFIX_ABN,
        OASIS_PREFIX_GLN,
        OASIS_PREFIX_DUNS,
    )

    capabilityPublisherID = serializers.CharField(required=False, max_length=512)
    capabilityPublisherUrl = serializers.CharField(required=False, max_length=1000)

    participantIdentifier = serializers.CharField(required=True, max_length=1024)
    participantIdentifierScheme = serializers.CharField(required=True, max_length=1024)

    def validate_capabilityPublisherID(self, value):  # NOQA
        """
        If user provided capability publisher then user claims that this publisher
        is owned by him and we require it
        Othervise user leaves capabilityPublisherID field empty/omited and can
        update only participant_ids which are provided in his auth.
        """
        if not value:
            return None
        user = self.context['request'].user
        assert user and user.is_authenticated()

        try:
            party = AccreditedParty.objects.get(
                id=value,
                accreditation_status=AccreditedParty.STATUS_ACCR
            )
        except AccreditedParty.DoesNotExist:
            raise serializers.ValidationError(
                "Given capabilityPublisherID is not available (you may leave it empty)"
            )

        # TODO: check if user have access to it (not implemented yet)
        if party.id not in self.context['request'].auth.get('accredited_parties', []):
            logger.warning(
                "User tried to access party %s with auth %s",
                party,
                self.context['request'].auth
            )
            raise serializers.ValidationError(
                "Given capabilityPublisherID is not available (you may leave it empty)"
            )

        return party

    def validate_participantIdentifierScheme(self, value):  # NOQA
        if value != value.strip():
            raise serializers.ValidationError("You must not use trailing spaces in participant identifier scheme")
        # The participant Identifier must meet the structural format
        #     requirements of the identifier scheme.
        # The participant identifier scheme must be on the Council's list of
        #     approved identifiers, as per the Policy on the use of business identifiers.
        if value not in self.SUPPORTED_SCHEMES and not value.startswith(OASIS_PREFIX_UNREGISTERED):
            raise serializers.ValidationError("Unsupported scheme (ABN, GLN, DUNS and unregistered are supported)")
        return value

    def validate(self, data):
        participant_id = None
        if 'participantIdentifier' in data and 'participantIdentifierScheme' in data:
            participant_id = "{}::{}".format(
                data['participantIdentifierScheme'],
                data['participantIdentifier']
            ).lower()
        if not participant_id:
            raise serializers.ValidationError("Can't determine ParticipantId to update")
        data['participant_id'] = participant_id

        # user must have either participant_id in his auth or party in his auth
        access_type = None
        user_auth = getattr(self.context['request'], 'auth') or {}

        available_participant_ids = user_auth.get('participant_ids', [])

        if participant_id in available_participant_ids:
            access_type = 'participant_id_owner'

        if data.get('capabilityPublisherID'):
            access_type = 'accredited_party_actor'
            # TODO: if it's ledger then they have access to anything
            # if it's JWT user then only to itself

        if not access_type:
            raise serializers.ValidationError(
                "You don't have access to this ParticipantId"
            )
        data['access_type'] = access_type

        data['new_value'] = self._get_new_value(data)

        self._validate_participant_id(data)

        self._validate_capability_publisher_dualism(data)
        return data

    def _validate_participant_id(self, data):
        # The participant must not have an active relationship with another DCP.
        #     If they do then an error must be returned.
        if data['access_type'] == 'accredited_party_actor':
            # PID owner can change to any value, DCP - only from empty to itself
            last_token = DclRecordUpdateToken.objects.filter(
                participant_id=data['participant_id']
            ).order_by('-id').first()
            if last_token:
                if last_token.new_value and last_token.new_value != data['new_value']:
                    raise serializers.ValidationError(
                        "Participant ID DCL record has conflicting value"
                    )
        return

    def _validate_capability_publisher_dualism(self, data):
        if not data.get('capabilityPublisherUrl') and not data.get('capabilityPublisherID'):
            raise serializers.ValidationError(
                "You must provide either capabilityPublisherID or capabilityPublisherUrl"
                " - impossible to update DCP value without DCP provided"
            )

        if data.get('capabilityPublisherUrl') and data.get('capabilityPublisherID'):
            raise serializers.ValidationError(
                "You must provide either capabilityPublisherID or capabilityPublisherUrl"
                " - not both at the same time"
            )

    def _get_new_value(self, data):
        new_value = None
        if data.get('capabilityPublisherUrl'):
            new_value = data.get('capabilityPublisherUrl')
        elif data.get('capabilityPublisherID'):
            new_value = data.get('capabilityPublisherID').dcp_host
        return new_value

    def save(self):
        new_value = self.validated_data['new_value']
        assert new_value

        logger.info(
            "User %s with access based on %s tries to update record %s to value %s",
            self.context['request'].user,
            self.validated_data.get('access_type'),
            self.validated_data.get('participant_id'),
            new_value
        )

        result = update_dcl_record(
            participant_id=self.validated_data['participant_id'],
            new_value=new_value,
            actor_party=self.validated_data.get('capabilityPublisherID'),
            actor_user=self.context['request'].user,
        )
        return result

    def get_response_data(self):
        return {
            "hash": "b-{}".format(get_hash(self.validated_data['participant_id']).lower())
        }


class DeleteDclRecordSerializer(UpdateDclRecordSerializer):
    def _validate_capability_publisher_dualism(self, data):
        return


class UpdateDclRecordView(generics.CreateAPIView, generics.DestroyAPIView):
    """
    Input format:
    {
        "participantIdentifier": "51824753556",
        "participantIdentifierScheme": "urn:oasis:names:tc:ebcore:partyid-type:iso6523:0151",
        "capabilityPublisherID": "1"
    }
    or (XML hasn'e been implemented yet)
    <RegisterCapabilityAddressForParticipant
        xmlns="http://busdox.org/serviceMetadata/locator/1.0/"
        xmlns:ids="http://busdox.org/transport/identifiers/1.0/">
        <CapabilityPublisherID>1</CapabilityPublisherID >
        <ids:ParticipantIdentifier scheme="urn:oasis:names:tc:ebcore:partyid-type:iso6523:0151">
        51824753556
        </ids:ParticipantIdentifier>
    </RegisterCapabilityAddressForParticipant >
    """

    def get_serializer_class(self):
        if self.request.method == 'DELETE':
            return DeleteDclRecordSerializer
        else:
            return UpdateDclRecordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.get_response_data(),
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class DeleteDclRecordView(generics.DestroyAPIView):

    def destroy(self, request, *args, **kwargs):
        participant_id = kwargs.get('participant_id')

        user_auth = getattr(request, 'auth', {}) or {}
        parties = user_auth.get('accredited_parties', [])

        for party in parties:
            last_token = DclRecordUpdateToken.objects.filter(
                participant_id=participant_id
            ).order_by('-id').first()
            if last_token:
                if last_token.new_value and last_token.new_value != party.dcp_host:
                    raise serializers.ValidationError(
                        "Participant ID DCL record has conflicting value"
                    )

        result = clear_dcl_record(participant_id)
        if result is True:
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return response.Response(
                {
                    "errors": [
                        {
                            "code": "DCL-X500",
                            "name": "Record Update Problem",
                            "userMessage": (
                                "It was impossible to delete such resource "
                                "(due it access problems or non-existance)"
                            )
                        }
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
