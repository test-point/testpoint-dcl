from django.conf.urls import url

from dcl_server.ausdigital_api_v0.views.common import DemoAuthView

from .views.acp import ACPListView, AccessPointsListView
from .views.update import CreateReplaceDclRecordView, UpdateDeleteDclRecordView

urlpatterns = [
    # helpers
    url(r'^demo_auth/?$', DemoAuthView.as_view(), name='demo-auth'),

    # DBC-compliant urls
    # update
    url(
        r'^capabilityPublishers?/(?P<capabilityPublisherID>[^/]+)/participants/?$',
        CreateReplaceDclRecordView.as_view(),
        name='dcl-record-create'
    ),
    # delete
    url(
        r'^capabilityPublishers?/(?P<capabilityPublisherID>[^/]+)/participants/(?P<participantId>[^/]+)/?$',
        UpdateDeleteDclRecordView.as_view(),
        name='dcl-record-details'
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
