from __future__ import unicode_literals
import logging

from rest_framework import generics, serializers, response, status

from dcl_server.backends.generic import update_dcl_record, clear_dcl_record
from dcl_server.oasis.constants import OASIS_PREFIX_PARTYID
from dcl_server.oasis.utils import get_hash

logger = logging.getLogger(__name__)


class UpdateDclRecordSerializer(serializers.Serializer):
    capabilityPublisherUrl = serializers.CharField(required=True, max_length=1000)
    participantIdentifier = serializers.CharField(required=True, max_length=1024)
    participantIdentifierScheme = serializers.CharField(required=True, max_length=1024)

    def validate_participantIdentifierScheme(self, value):  # NOQA
        if value != value.strip():
            raise serializers.ValidationError("You must not use trailing spaces in participant identifier scheme")
        # The participant Identifier must meet the structural format
        #     requirements of the identifier scheme.
        # The participant identifier scheme must be on the Council's list of
        #     approved identifiers, as per the Policy on the use of business identifiers.
        if not value.startswith(OASIS_PREFIX_PARTYID):
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

        # user must have participant_id in his auth
        user_auth = getattr(self.context['request'], 'auth') or {}
        available_participant_ids = user_auth.get('participant_ids', [])
        if participant_id not in available_participant_ids:
            raise serializers.ValidationError(
                "You don't have access to this ParticipantId"
            )
        return data

    def save(self):
        new_value = self.validated_data['capabilityPublisherUrl']
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


class UpdateDclRecordView(generics.CreateAPIView):
    """
    Input format:
    {
        "participantIdentifier": "51824753556",
        "participantIdentifierScheme": "urn:oasis:names:tc:ebcore:partyid-type:iso6523:0151",
        "capabilityPublisherUrl": "dcp.testpoint.io"
    }
    """

    def get_serializer_class(self):
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
        available_participant_ids = user_auth.get('participant_ids', [])
        if participant_id not in available_participant_ids:
            raise serializers.ValidationError(
                "You don't have access to this ParticipantId"
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
