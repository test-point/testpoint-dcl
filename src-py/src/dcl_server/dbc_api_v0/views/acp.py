from __future__ import unicode_literals
import logging

from rest_framework import generics, serializers, permissions

from dcl_server.accreditations.models import AccreditedParty

logger = logging.getLogger(__name__)


class ACPDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccreditedParty
        fields = (
            'id', 'service_provider_id', 'trading_name', 'contact_email',
            'registration_url', 'dcp_host', 'created', 'accreditation_status'
        )

    def to_representation(self, instance):
        data = super(ACPDetailsSerializer, self).to_representation(instance)
        data['CapabilityPublisherID'] = data['id']
        del data['id']
        data['ServerCertificates'] = instance.valid_certificates['client']
        data['ClientCertificates'] = instance.valid_certificates['server']
        return data


class AccessPointDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccreditedParty
        fields = (
            'id', 'service_provider_id', 'trading_name', 'contact_email',
            'registration_url', 'dcp_host', 'created', 'accreditation_status'
        )

    def to_representation(self, instance):
        data = super(AccessPointDetailsSerializer, self).to_representation(instance)
        data['AccessPointID'] = data['id']
        del data['id']
        data['ServerCertificates'] = instance.valid_certificates['client']
        data['ClientCertificates'] = instance.valid_certificates['server']
        return data


class ACPListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ACPDetailsSerializer

    def get_queryset(self):
        qs = AccreditedParty.objects.filter(
            accreditation_status=AccreditedParty.STATUS_ACCR
        )
        try:
            if self.request.GET.get('service_provider_id', '').strip():
                qs = qs.filter(
                    service_provider_id=self.request.GET['service_provider_id']
                )
        except (ValueError, TypeError):
            pass
        try:
            if self.request.GET.get('id', '').strip():
                qs = qs.filter(
                    id=self.request.GET['id']
                )
        except (ValueError, TypeError):
            pass
        if self.request.GET.get('name', '').strip():
            qs = qs.filter(
                trading_name=self.request.GET['name']
            )
        return qs


class AccessPointsListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AccessPointDetailsSerializer

    def get_queryset(self):
        qs = AccreditedParty.objects.filter(
            accreditation_status=AccreditedParty.STATUS_ACCR
        )
        try:
            if self.request.GET.get('service_provider_id', '').strip():
                qs = qs.filter(
                    service_provider_id=self.request.GET['service_provider_id']
                )
        except (ValueError, TypeError):
            pass
        try:
            if self.request.GET.get('id', '').strip():
                qs = qs.filter(
                    id=self.request.GET['id']
                )
        except (ValueError, TypeError):
            pass
        if self.request.GET.get('name', '').strip():
            qs = qs.filter(
                trading_name=self.request.GET['name']
            )
        return qs