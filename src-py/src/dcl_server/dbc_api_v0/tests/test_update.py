from __future__ import unicode_literals

import mock
import pytest

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from dcl_server.accreditations.models import UserPartyAccess
from dcl_server.accreditations.factories import AccreditedPartyFactory
from dcl_server.dcl_audit.models import DclRecordUpdateToken

from dcl_server.utils.tests import do_jwt_request


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
        reverse('dbc-api-v0:update-dcl-record', args=[acp.id]),
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
    new_user = get_user_model().objects.get(username='simguard_{}'.format(id_value))

    UserPartyAccess.objects.create(
        user=new_user,
        party=acp
    )

    # shall have access now
    resp = do_jwt_request(
        "urn:oasis:names:tc:ebcore:partyid-type:iso6523:0151::" + id_value,
        'post',
        reverse('dbc-api-v0:update-dcl-record', args=[acp.id]),
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
@mock.patch('dcl_server.backends.route53.DnsBackend.clear_dcl')
def test_record_delete(backend_mock, admin_user, admin_client):
    # TODO: check if request proxy everything fine till deep backend
    # TODO: check errors for:
    # * auth
    # * wrong url/payload parameters
    # * access to given Party
    assert DclRecordUpdateToken.objects.count() == 0

    admin_client.delete(
        reverse(
            'dbc-api-v0:delete-dcl-record',
            args=[1, 'urn:oasis:names:tc:ebcore:partyid-type:iso6523:0151::51824753556']
        )
    )

    assert backend_mock.call_count == 1
    assert DclRecordUpdateToken.objects.count() == 1
    assert not DclRecordUpdateToken.objects.first().new_value
