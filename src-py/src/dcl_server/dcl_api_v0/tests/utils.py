from __future__ import unicode_literals

import mock
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

OASIS_PREFIX_ISO = 'urn:oasis:names:tc:ebcore:partyid-type:iso6523'


def do_jwt_request(jwt_pid, method='get', *args, **kwargs):
    api_client = APIClient()
    if jwt_pid:
        if isinstance(jwt_pid, (str, unicode)):
            jwt_pid = [jwt_pid]

        oasis_claims = []
        for jwt_pid_row in jwt_pid:
            pid_scheme, pid_value = jwt_pid_row.replace(OASIS_PREFIX_ISO + ':', '').split('::')
            oasis_claims.append({pid_scheme: pid_value})

        # ensure we have some users
        if get_user_model().objects.count() == 0:
            get_user_model().objects.create(username='simguard_{}'.format(oasis_claims[0].items()[0][1]))

        auth_result = (
            get_user_model().objects.first(),
            {
                'iss': 'http://127.0.0.1:7500',
                'sub': oasis_claims[0].items()[0][1],
                OASIS_PREFIX_ISO: oasis_claims,
            }
        )

        kwargs['headers'] = kwargs.get('headers', {})
        kwargs['headers']['Authorization'] = 'JWT somedumbstuff'
        with mock.patch("dcl_server.dcl_api_v0.authentication.MultipleProvidersJWTAuthentication.authenticate") as mocked_auth:
            mocked_auth.return_value = auth_result
            resp = getattr(api_client, method)(
                *args, **kwargs
            )
    else:
        # plain request
        resp = getattr(api_client, method)(
            *args, **kwargs
        )
    return resp
