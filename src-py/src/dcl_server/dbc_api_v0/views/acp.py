from __future__ import unicode_literals
import logging

from rest_framework import generics, serializers, permissions

from dcl_server.accreditations.models import AccreditedParty

logger = logging.getLogger(__name__)


class ACPDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccreditedParty
        fields = (
            'service_provider_id', 'trading_name', 'contact_email',
            'registration_url', 'created', 'accreditation_status'
            # 'accreditation_status', 'dcp_host',
        )

    def to_representation(self, instance):
        data = super(ACPDetailsSerializer, self).to_representation(instance)
        data['CapabilityPublisherID'] = data.pop('service_provider_id')

        data['name'] = data.pop('trading_name')
        data['contactEmail'] = data.pop('contact_email')
        data['URL'] = data.pop('registration_url')

        data['accreditationStatus'] = data.pop('accreditation_status')

        data['ServerCertificates'] = instance.valid_certificates['client']
        data['ClientCertificates'] = instance.valid_certificates['server']
        return data


class AccessPointDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccreditedParty
        fields = (
            'service_provider_id', 'trading_name', 'contact_email',
            'registration_url', 'dcp_host', 'created', 'accreditation_status'
        )

    def to_representation(self, instance):
        data = super(AccessPointDetailsSerializer, self).to_representation(instance)
        data['AccessPointID'] = data.pop('service_provider_id')
        data['name'] = data.pop('trading_name')
        data['contactEmail'] = data.pop('contact_email')
        data['URL'] = data.pop('registration_url')
        data['dcpHost'] = data.pop('dcp_host')
        data['accreditationStatus'] = data.pop('accreditation_status')

        data['ServerCertificates'] = instance.valid_certificates['client']
        data['ClientCertificates'] = instance.valid_certificates['server']
        return data


class ACPListView(generics.ListAPIView):
    """List Accredited Digital Capability Publishers"""

    permission_classes = (permissions.AllowAny,)
    serializer_class = ACPDetailsSerializer

    def get_queryset(self):
        qs = AccreditedParty.objects.filter(
            accreditation_status=AccreditedParty.STATUS_ACCR
        )

        filter_id = self.request.GET.get('id', '').strip()
        filter_name = self.request.GET.get('name', '').strip()
        if filter_id:
            qs = qs.filter(
                service_provider_id__contains=filter_id
            )
        if filter_name:
            qs = qs.filter(
                trading_name__contains=filter_name
            )
        return qs


class AccessPointsListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AccessPointDetailsSerializer

    def get_queryset(self):
        qs = AccreditedParty.objects.filter(
            accreditation_status=AccreditedParty.STATUS_ACCR
        )
        filter_id = self.request.GET.get('id', '').strip()
        filter_name = self.request.GET.get('name', '').strip()
        if filter_id:
            qs = qs.filter(
                service_provider_id__contains=filter_id
            )
        if filter_name:
            qs = qs.filter(
                trading_name__contains=filter_name
            )
        return qs
