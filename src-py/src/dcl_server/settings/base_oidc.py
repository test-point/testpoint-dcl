from envparse import env

# our hostname is required for some OIDC processes
HOSTNAME = env("DCL_HOSTNAME", default='http://127.0.0.1:5200')
if HOSTNAME.endswith('/'):
    HOSTNAME = HOSTNAME[:-1]

# default values for localhost, feel free to use it; safe to be spoiled to Github - nobody can use it except for localhost.
SIMGUARD_HOSTNAME = env("DCL_SIMGUARD_HOSTNAME", default='https://idp.testpoint.io')
SIMGUARD_CLIENT_ID = env("DCL_SIMGUARD_CLIENT_ID", default='999999')
SIMGUARD_CLIENT_SECRET = env("DCL_SIMGUARD_CLIENT_SECRET", default='some value; check out IDP.testpoint.io to details how to get one')

if SIMGUARD_HOSTNAME.endswith('/'):
    SIMGUARD_HOSTNAME = SIMGUARD_HOSTNAME[:-1]

# Default is using the 'code' workflow, which requires direct connectivity from your website to the OP.
OIDC_DEFAULT_BEHAVIOUR = {
    "response_type": "code",
    "scope": ["openid", "profile", "email", "address", "phone"],
}

OIDC_ALLOW_DYNAMIC_OP = False

OIDC_PROVIDERS = {
    'SimGuard': {
        'provider_info': {
            # provider info may be fetched automatically from the taget OIDC provider,
            # but it doesn't work well with zappa due to increased lag
            # so, the result for idp.testpoint.io cached here.
            "userinfo_endpoint": "{}/userinfo".format(SIMGUARD_HOSTNAME),
            "jwks_uri": "{}/jwks".format(SIMGUARD_HOSTNAME),
            "subject_types_supported": ["public"],
            "token_endpoint": "{}/token".format(SIMGUARD_HOSTNAME),
            "id_token_signing_alg_values_supported": ["HS256", "RS256"],
            "token_endpoint_auth_methods_supported": ["client_secret_post", "client_secret_basic"],
            "response_types_supported": ["code", "id_token", "id_token token"],
            "end_session_endpoint": "{}/logout".format(SIMGUARD_HOSTNAME),
            "authorization_endpoint": "{}/authorize".format(SIMGUARD_HOSTNAME),
            "issuer": "{}".format(SIMGUARD_HOSTNAME)
        },
        "behaviour": OIDC_DEFAULT_BEHAVIOUR,
        "client_registration": {
            "client_id": SIMGUARD_CLIENT_ID,
            "client_secret": SIMGUARD_CLIENT_SECRET,
            "redirect_uris": [HOSTNAME + "/oidc/authz/"],
            "post_logout_redirect_uris": [HOSTNAME + "/"],
        },
    },
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'dcl_server.auth_backends.OpenIdConnectAndRegisterBackend',
]


# for DRF stuff
OIDC_AUTH = {
    'OIDC_ENDPOINTS': {
        'default': {
            'issuer': 'default',
            'endpoint': env('DCL_OIDC_ENDPOINT', default=SIMGUARD_HOSTNAME),
            'audiences': env('DCL_OIDC_AUDIENCES', default=SIMGUARD_CLIENT_ID).split(','),
        }
    },

    # Specify OpenID Connect endpoint. Configuration will be
    # automatically done based on the discovery document found
    # at <endpoint>/.well-known/openid-configuration
    'OIDC_ENDPOINT': env('DCL_OIDC_ENDPOINT', default=SIMGUARD_HOSTNAME),
    'OIDC_AUDIENCES': env('DCL_OIDC_AUDIENCES', default=SIMGUARD_CLIENT_ID).split(','),
    'OIDC_RESOLVE_USER_FUNCTION': 'dcl_server.dcl_api_v0.authentication.get_oidc_drf_user',
    'OIDC_LEEWAY': 3600 * 48,
    'OIDC_JWKS_EXPIRATION_TIME': 24 * 60 * 60,
    'OIDC_BEARER_TOKEN_EXPIRATION_TIME': 60 * 10,
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'BEARER_AUTH_HEADER_PREFIX': 'Bearer',
}

DRFOIDC_ENDPOINTS_CONF = env("DCL_DRFOIDC_ENDPOINTS_CONF", default=None)
if DRFOIDC_ENDPOINTS_CONF:
    # new-style packed configuration item
    # conf example:
    #  readablename;issuer;endpoint;audience1,audience2|
    #  simguard;https://idp.testpoint.io;https://idp.testpoint.io;928680,242989,697856|
    #  loa1dbc;http://127.0.0.1:7555;http://127.0.0.1:7555;671905|
    for idp_row in DRFOIDC_ENDPOINTS_CONF.split('|'):
        readable_name, issuer, endpoint, audiences = idp_row.split(';')
        audiences = audiences.split(',')
        # TODO: provider_info support, to avoid extra HTTPS request every time
        OIDC_AUTH['OIDC_ENDPOINTS'][readable_name] = {
            'issuer': issuer,
            'endpoint': endpoint,
            'audiences': audiences,
        }
    del OIDC_AUTH['OIDC_ENDPOINTS']['default']
else:
    # old-style mockery
    pass
