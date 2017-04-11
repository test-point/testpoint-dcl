import json
import logging
import pprint  # NOQA

import requests
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from jwkest.jws import JWSig
from jwkest.jwk import KEYS
from rest_framework import authentication, exceptions, permissions
from oidc_auth.authentication import JSONWebTokenAuthentication
from oidc_auth.settings import api_settings

from dcl_server.accreditations.models import UserPartyAccess

logger = logging.getLogger(__name__)


def get_oidc_drf_user(request, id_token):
    issuer_readable_name = "some_idp"
    for readable_name, possible_issuer_row in settings.OIDC_AUTH['OIDC_ENDPOINTS'].items():
        if possible_issuer_row['issuer'] == id_token.get('iss'):
            issuer_readable_name = readable_name
    user_class = get_user_model()
    # TODO: different username for different IDP
    natural_key = "{}_{}".format(issuer_readable_name, id_token.get('sub'))
    try:
        user = user_class.objects.get_by_natural_key(natural_key)
    except user_class.DoesNotExist:
        email_prepared = id_token['iss'].replace('https://', '').replace('http://', '')
        user = user_class.objects.create(
            username=natural_key,
            email='{}@{}'.format(id_token['sub'], email_prepared),
        )
        logger.info("User %s with auth %s has been created", natural_key, id_token)
    user.last_login = timezone.now()
    user.save()
    return user


class MultipleProvidersJWTAuthentication(JSONWebTokenAuthentication):

    issuer_name = 'default'
    issuer_config = None

    def __init__(self, *args, **kwargs):
        self.settings = api_settings
        return super(MultipleProvidersJWTAuthentication, self).__init__(*args, **kwargs)

    @property
    def oidc_config(self):
        """
        Now we try to get correct issuer configuration.
        Side-effect requirement: self.issuer_name set to correct value (or default is provided)
        """
        if (self.issuer_name != 'default') or ('default' in self.settings.OIDC_ENDPOINTS):
            # new settings file
            self.issuer_config = self.settings.OIDC_ENDPOINTS[self.issuer_name]
            endpoint = self.issuer_config['endpoint']
        else:
            # legacy settings file
            endpoint = self.settings.OIDC_ENDPOINT
            self.issuer_config = None

        if self.issuer_config and 'provider_info' in self.issuer_config:
            # if the config has been provided statically or already loaded
            config = self.issuer_config['provider_info']
        else:
            config = self.fetch_remote_oidc_config(endpoint)
            if self.issuer_config:
                # cache the result in issuer_config itself
                self.issuer_config['provider_info'] = config
            else:
                # just return what we got without any caching
                # (assume fetch_remote_oidc_config caches it)
                pass
        return config

    def fetch_remote_oidc_config(self, endpoint):
        return requests.get(endpoint + '/.well-known/openid-configuration').json()

    def jwks(self):
        # TODO: some cache with respect of self.issuer_config
        # now keys are being reloaded every time
        # (doesn't matter for Zappa until keys are cached to Redis)
        keys = KEYS()
        keys.load_from_url(self.oidc_config['jwks_uri'])
        return keys

    @property
    def issuer(self):
        # duplicated to disable the cache - self.oidc_config handles that
        return self.oidc_config['issuer']

    def authenticate(self, request):
        try:
            # here we quickly look into the JWT token, without any validation, to get issuer
            # because our next behaviour depends on issuer (verification urls, etc)
            jwt_value = self.get_jwt_value(request)
            if jwt_value is None:
                return None  # not OIDC JWT auth
            try:
                target_issuer = json.loads(
                    JWSig().unpack(jwt_value).part[1]
                )['iss']
            except (UnicodeDecodeError, ValueError):
                raise exceptions.AuthenticationFailed("Badly formed JWT")

            # if we got to this point - JWT is valid, and issuer in `target_issuer` variable.
            for issuer_name, issuer_config in self.settings.OIDC_ENDPOINTS.items():
                if issuer_config['issuer'] == target_issuer:
                    self.issuer_name = issuer_name
                    break
            if self.issuer_name is None:
                raise exceptions.AuthenticationFailed(
                    'Invalid Authorization header. Invalid JWT issuer. Not found in the whitelist'
                )
        except Exception as e:
            logger.exception(e)
            # nasty JWT
            # okay, let's assume we can't determine the issuer, so just fall back to legacy behaviour
            pass

        try:
            auth_result = super(MultipleProvidersJWTAuthentication, self).authenticate(request)
        except (UnicodeDecodeError, ValueError):
            raise exceptions.AuthenticationFailed("Badly formed JWT")
        return auth_result

    def get_audiences(self, id_token):
        if self.issuer_config is None:
            # legacy configuration
            aud = api_settings.OIDC_AUDIENCES
        else:
            aud = self.issuer_config['audiences']
        return aud


class ProvideParticipantPermission(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        if not super(ProvideParticipantPermission, self).has_permission(request, view):
            return False
        if request.user is None:
            raise exceptions.AuthenticationFailed(
                "You need to provide valid authentication to use this endpoint"
            )
        if not request.user.is_authenticated():
            raise exceptions.AuthenticationFailed(
                "Can't determine user related to this auth"
            )
        if request.auth is None:
            request.auth = {}
        # determine the participant IDs from given user/auth
        request.auth['participant_ids'] = get_participant_ids_for_auth(request.auth, request.user)
        # TODO: determine which Accredited Parties this JWT can access
        request.auth['accredited_parties'] = set(list(
            UserPartyAccess.objects.filter(
                is_active=True,
                user=request.user
            ).distinct().values_list('party_id', flat=True)
        ))
        return True

    def has_object_permission(self, request, view, obj):
        # return request.user == obj.user
        return False


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


def get_participant_ids_for_auth(auth, user=None):
    """
    Return list of businessed IDS for this user.
    Assuming AUTH contains some business user info, and user can be filled
    with all related objects.

    Output example for user owning ABN 15304860073:
        [
            "urn:oasis:names:tc:ebcore:partyid-type:iso6523:0151::15304860073"
        ]
    This value can be converted to hashes and queried/displayed to user.

    TODO: normalize it (not only lower)
    """
    participant_ids = []

    # super new style: participant_ids list
    iso_pid_prefix = 'urn:oasis:names:tc:ebcore:partyid-type:iso6523'
    if not auth:
        return participant_ids
    urnstyle_pids = auth.get(iso_pid_prefix, [])
    if isinstance(urnstyle_pids, list):
        for pid_row_dict in urnstyle_pids:
            if len(pid_row_dict.keys()) == 1:
                id_scheme, id_value = pid_row_dict.items()[0]
                if isinstance(id_scheme, (unicode, str)) and isinstance(id_value, (unicode, str)):
                    participant_ids.append(u"{}:{}::{}".format(iso_pid_prefix, id_scheme, id_value).lower())
    return participant_ids


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
