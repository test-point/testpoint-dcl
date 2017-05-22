from django.conf.urls import url

from .views.common import DemoAuthView, HealthcheckView
from .views.update import UpdateDclRecordView

urlpatterns = [
    # helpers
    url(r'^demo_auth/?$', DemoAuthView.as_view(), name='demo-auth'),
    url(r'^healthcheck/?$', HealthcheckView.as_view(), name='healthcheck'),
    url(r'^dcl-record/?$', UpdateDclRecordView.as_view(), name='update-dcl-record'),
]
