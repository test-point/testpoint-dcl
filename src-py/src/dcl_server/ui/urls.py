from django.conf.urls import url

from .views import IndexUiView

urlpatterns = [
    url(r'^$', IndexUiView.as_view(), name='index'),
]
