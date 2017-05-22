import logging
import pprint  # NOQA

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import authentication, exceptions

from dcl_server.ausdigital_api_v0.authentication import ProvideParticipantPermission

logger = logging.getLogger(__name__)


class RequireASP(ProvideParticipantPermission):
    def has_permission(self, request, view):
        is_authenticated = super(RequireASP, self).has_permission(request, view)
        if not is_authenticated:
            return False
        # it's authenticated at least
        if not request.auth['accredited_parties']:
            raise exceptions.AuthenticationFailed(
                "The Accredited Service Provider is required to access this API Endpoint"
            )
        return True


class ClientCertificateAuth(authentication.BaseAuthentication):
    VERIFIED_SUCCESS = 'SUCCESS'

    def parse_dn(self, dn):
        """
        http://www.ietf.org/rfc/rfc4514.txt
          CN      commonName (2.5.4.3)
          L       localityName (2.5.4.7)
          ST      stateOrProvinceName (2.5.4.8)
          O       organizationName (2.5.4.10)
          OU      organizationalUnitName (2.5.4.11)
          C       countryName (2.5.4.6)
          STREET  streetAddress (2.5.4.9)
          DC      domainComponent (0.9.2342.19200300.100.1.25)
          UID     userId (0.9.2342.19200300.100.1.1)

        {
            'C': 'AU', 'CN': 'dcp-testpoint-io-certuser', 'L': 'Default City',
            'O': 'dcp.testpoint.io', 'ST': 'Melbourne',
            'emailAddress': 'hi@testpoint.io', 'OU': 'dcp-section'
        }
        /C=AU/ST=Melbourne/L=Default City/O=dcp.testpoint.io/OU=dcp-section/CN=dcp-testpoint-io-certuser/emailAddress=hi@testpoint.io
        """
        return dict((part.split('=') for part in dn.split('/') if '=' in part))

    def authenticate(self, request):
        # TODO: fail if request is made with http, not https
        http_verified = request.META.get('HTTP_VERIFIED')
        if http_verified == self.VERIFIED_SUCCESS:
            # the certificate is fine! as nginx thinks at least
            http_dn = request.META.get('HTTP_DN')
            dn = self.parse_dn(http_dn)

            user = self.get_user(dn)
            if user is None:
                raise exceptions.AuthenticationFailed('No user created for this certificate')
            return (user, dn)
        return None

    def get_user(self, dn):
        user_class = get_user_model()
        assert 'CN' in dn
        natural_key = "tls_{}".format(dn['CN'])
        try:
            user = user_class.objects.get_by_natural_key(natural_key)
        except user_class.DoesNotExist:
            user = user_class.objects.create(
                username=natural_key,
                email=dn.get('emailAddress'),
            )
        user.last_login = timezone.now()
        user.save()
        return user
