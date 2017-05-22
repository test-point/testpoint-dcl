from djangooidc.backends import OpenIdConnectBackend


class OpenIdConnectAndRegisterBackend(OpenIdConnectBackend):

    def authenticate(self, **kwargs):
        user = super(OpenIdConnectAndRegisterBackend, self).authenticate(**kwargs)
        return user

    def clean_username(self, sub):
        # TODO: once we support login with multiple OIDC providers this code
        # will be a little more complex to reflect it
        return 'idp_{}'.format(sub)
