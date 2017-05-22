from __future__ import unicode_literals

# import mock
import pytest

# from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

# from dcl_server.accreditations.models import UserPartyAccess
from dcl_server.accreditations.factories import AccreditedPartyFactory
# from dcl_server.dcl_audit.models import DclRecordUpdateToken


@pytest.mark.django_db
def test_fetch_acp_list_access(admin_user, admin_client):
    ap1 = AccreditedPartyFactory()

    # # no access error expected (user doesn't have any access to any ACP)
    # resp = admin_client.get(
    #     reverse('api-v0:acp-list'),
    #     format="json",
    # )
    # print(resp.content)
    # assert resp.status_code == 403
    # assert resp.json() == {
    #     "detail": "The Accredited Service Provider is required to access this API Endpoint"
    # }

    # UserPartyAccess.objects.create(
    #     party=ap1,
    #     user=admin_user
    # )

    resp = admin_client.get(
        reverse('dbc-api-v0:acp-list'),
        format="json",
    )
    print(resp.content)
    assert resp.status_code == 200
    assert resp.json()['results'][0]['CapabilityPublisherID'] == ap1.service_provider_id
