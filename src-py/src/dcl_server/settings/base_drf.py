REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        # 'rest_framework_xml.parsers.XMLParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'dcl_server.ausdigital_api_v0.renderers.PrettyJsonRenderer',
        'rest_framework_xml.renderers.XMLRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # http://blog.nategood.com/client-side-certificate-authentication-in-ngi
        'dcl_server.dbc_api_v0.authentication.ClientCertificateAuth',
        'dcl_server.ausdigital_api_v0.authentication.MultipleProvidersJWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'dcl_server.ausdigital_api_v0.authentication.ProvideParticipantPermission',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50
}
