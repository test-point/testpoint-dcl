from djangooidc.backends import OpenIdConnectBackend


class OpenIdConnectAndRegisterBackend(OpenIdConnectBackend):

    def authenticate(self, **kwargs):
        user = super(OpenIdConnectAndRegisterBackend, self).authenticate(**kwargs)
        # # update our local profile every login
        # if user is not None:
        #     user.business.extra_data = kwargs
        #     user.business.auth_source = user.business.AUTH_SIMGUARD
        #     user.business.save()
        return user

    def clean_username(self, sub):
        # TODO: how to get if it simguard or vanguard?
        # theoretically possible by kwargs (data from IDC), but not rock-solid
        return 'idp_{}'.format(sub)
