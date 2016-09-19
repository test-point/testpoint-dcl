# encoding: utf-8
from django.conf.urls import url


def openid_proxy(*args, **kwargs):
    from djangooidc.views import openid
    return openid(*args, **kwargs)


def proxy_authz_cb(*args, **kwargs):
    from djangooidc.views import authz_cb
    return authz_cb(*args, **kwargs)


def proxy_logout(*args, **kwargs):
    from djangooidc.views import logout
    return logout(*args, **kwargs)


def proxy_logout_cb(*args, **kwargs):
    from djangooidc.views import logout_cb
    return logout_cb(*args, **kwargs)


urlpatterns = [
    # url(r'^openid/login/?$', openid_proxy, name='openid'),
    url(r'^openid/openid/(?P<op_name>[^/]+)/?$', openid_proxy, name='openid_with_op_name'),
    url(r'^openid/callback/login/?$', proxy_authz_cb, name='openid_login_cb'),
    url(r'^openid/logout/?$', proxy_logout, name='logout'),
    url(r'^openid/callback/logout/?$', proxy_logout_cb, name='openid_logout_cb'),
    url(r'^oidc/authz/?$', proxy_authz_cb, name='vanguard_callback_1'),
    url(r'^rp/callback/?$', proxy_authz_cb, name='vanguard_callback_1'),
]
