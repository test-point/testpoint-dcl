"""dcl_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='http://testpoint.io/dcl.html'), name='index'),
    url(r'^ui/', include('dcl_server.ui.urls', namespace='ui')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', RedirectView.as_view(url='/openid/openid/SimGuard/?next=/ui/'), name='login'),
    url(r'', include('dcl_server.djangooidc_proxy_urls')),
]
