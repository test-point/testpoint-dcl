from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView


urlpatterns = [
    url(r'^ui/', include('dcl_server.ui.urls', namespace='ui')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', RedirectView.as_view(url='/openid/openid/SimGuard/?next=/ui/'), name='login'),
    url(r'^api/v0/', include('dcl_server.dcl_api_v0.urls', namespace='api-v0')),

    url(r'', include('dcl_server.djangooidc_proxy_urls')),
]

if settings.DEBUG is False:
    urlpatterns.insert(
        0,
        url(r'^$', RedirectView.as_view(url='http://testpoint.io/dcl.html'), name='index'),
    )
