from django.conf.urls import url

from .views.acp import ACPListView, AccessPointsListView
from .views.common import DemoAuthView, HealthcheckView
from .views.update import UpdateDclRecordView

urlpatterns = [
    # helpers
    url(r'^demo_auth/?$', DemoAuthView.as_view(), name='demo-auth'),
    url(r'^healthcheck/?$', HealthcheckView.as_view(), name='healthcheck'),

    # our simplified urls
    url(r'^dcl-record/?$', UpdateDclRecordView.as_view(), name='update-dcl-record'),

    # DBC-compliant urls
    # update/delete participant DCL record
    url(
        r'^capabilityPublishers?/(?P<capabilityPublisherID>[^/]+)/participants/?$',
        UpdateDclRecordView.as_view(),
        name='update-dcl-record-dbc'
    ),
    url(
        r'^capabilityPublishers?/(?P<capabilityPublisherID>[^/]+)/participants/(?P<participantId>[^/]+)/?$',
        UpdateDclRecordView.as_view(),
        name='update-dcl-record-dbc'
    ),
    # list of eDelivery DCPs that hold a current accreditation
    url(
        r'^capabilityPublishers?/?$',
        ACPListView.as_view(),
        name='acp-list'
    ),
    # list of eDelivery Access Points that hold a current accreditation
    url(
        r'^accessPoints?/?$',
        AccessPointsListView.as_view(),
        name='accesspoint-list'
    ),
]
