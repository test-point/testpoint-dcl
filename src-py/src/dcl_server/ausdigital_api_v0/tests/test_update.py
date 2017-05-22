from __future__ import unicode_literals

import mock
import pytest

from django.core.urlresolvers import reverse

from dcl_server.dcl_audit.models import DclRecordUpdateToken

from dcl_server.utils.tests import do_jwt_request


@pytest.mark.django_db
@mock.patch('dcl_server.backends.route53.DnsBackend.update_dcl')
def test_update_dcl_record_dcpurl(backend_mock, admin_user):
    assert backend_mock.call_count == 0
    assert DclRecordUpdateToken.objects.count() == 0

    # try to create some record without access to that party
    resp = do_jwt_request(
        "urn:oasis:names:tc:ebcore:partyid-type:iso6523:0151::51824753556",
        'post',
        reverse('ausdigital-api-v0:update-dcl-record'),
        data={
            "participantIdentifier": "51824753556",
            "participantIdentifierScheme": "urn:oasis:names:tc:ebcore:partyid-type:iso6523:0151",
            "capabilityPublisherID": "1"
        },
        format='json'
    )
    print(resp.content)
    assert resp.status_code == 400
    assert resp.json() == {
        "capabilityPublisherID": [
            "Given capabilityPublisherID is not available (you may leave it empty)"
        ]
    }

    assert backend_mock.call_count == 0
    assert DclRecordUpdateToken.objects.count() == 0

    # ok, we don't have it
    # try to just update my own
    resp = do_jwt_request(
        "urn:oasis:names:tc:ebcore:partyid-type:iso6523:0151::51824753556",
        'post',
        reverse('ausdigital-api-v0:update-dcl-record'),
        data={
            "participantIdentifier": "51824753556",
            "participantIdentifierScheme": "urn:oasis:names:tc:ebcore:partyid-type:iso6523:0151",
            "capabilityPublisherUrl": "some-dcl.testpoint.io"
        },
        format='json'
    )
    print(resp.content)
    assert resp.status_code == 201
    assert resp.json() == {
        "hash": "b-ef1067ff41f0b4885eea42ab0548659e"
    }

    assert backend_mock.call_count == 1
    assert DclRecordUpdateToken.objects.count() == 1
