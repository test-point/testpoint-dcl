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
