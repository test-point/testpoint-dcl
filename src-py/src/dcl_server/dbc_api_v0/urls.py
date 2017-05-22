from django.conf.urls import url

from dcl_server.ausdigital_api_v0.views.common import DemoAuthView

from .views.acp import ACPListView, AccessPointsListView
from .views.update import UpdateDclRecordView

urlpatterns = [
    # helpers
    url(r'^demo_auth/?$', DemoAuthView.as_view(), name='demo-auth'),

    # DBC-compliant urls
    # update/delete participant DCL record
    url(
        r'^capabilityPublishers?/(?P<capabilityPublisherID>[^/]+)/participants/?$',
        UpdateDclRecordView.as_view(),
        name='update-dcl-record'
    ),
    url(
        r'^capabilityPublishers?/(?P<capabilityPublisherID>[^/]+)/participants/(?P<participantId>[^/]+)/?$',
        UpdateDclRecordView.as_view(),
        name='update-dcl-record'
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
