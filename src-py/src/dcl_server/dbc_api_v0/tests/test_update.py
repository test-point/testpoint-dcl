from __future__ import unicode_literals

import mock
import pytest

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from dcl_server.accreditations.models import UserPartyAccess
from dcl_server.accreditations.factories import AccreditedPartyFactory
from dcl_server.dcl_audit.models import DclRecordUpdateToken


from .utils import do_jwt_request


@pytest.mark.django_db
@mock.patch('dcl_server.backends.route53.DnsBackend.update_dcl')
def test_update_dcl_record_dcpurl(backend_mock, admin_user):
    assert backend_mock.call_count == 0
    assert DclRecordUpdateToken.objects.count() == 0

    # try to create some record without access to that party
    resp = do_jwt_request(
        "urn:oasis:names:tc:ebcore:partyid-type:iso6523:0151::51824753556",
        'post',
        reverse('api-v0:update-dcl-record'),
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
        reverse('api-v0:update-dcl-record'),
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


@pytest.mark.django_db
@mock.patch('dcl_server.backends.route53.DnsBackend.update_dcl')
def test_update_dcl_record_partyid(backend_mock):
    assert backend_mock.call_count == 0
    assert DclRecordUpdateToken.objects.count() == 0

    acp = AccreditedPartyFactory()
    id_value = '51824753556'

    # try to create some record without access to that party
    resp = do_jwt_request(
        "urn:oasis:names:tc:ebcore:partyid-type:iso6523:0151::" + id_value,
        'post',
        reverse('api-v0:update-dcl-record'),
        data={
            "participantIdentifier": id_value,
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

    # give access to that party for latest created user
    print(list(get_user_model().objects.all().values_list('username', flat=True)))

    new_user = get_user_model().objects.get(username='simguard_{}'.format(id_value))

    UserPartyAccess.objects.create(
        user=new_user,
        party=acp
    )

    # shall have access now
    resp = do_jwt_request(
        "urn:oasis:names:tc:ebcore:partyid-type:iso6523:0151::" + id_value,
        'post',
        reverse('api-v0:update-dcl-record'),
        data={
            "participantIdentifier": id_value,
            "participantIdentifierScheme": "urn:oasis:names:tc:ebcore:partyid-type:iso6523:0151",
            "capabilityPublisherID": "1"
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


@pytest.mark.django_db
@pytest.mark.skip
def test_record_delete():
    # TODO: check if request proxy everything fine till deep backend
    # TODO: check errors for:
    # * auth
    # * wrong url/payload parameters
    # * access to given Party
    return
