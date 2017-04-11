from __future__ import unicode_literals

# from django.contrib.auth import get_user_model
from dcl_server.backends.route53 import DnsBackend
# from dcl_server.accreditations.models import AccreditedParty
from dcl_server.dcl_audit.models import DclRecordUpdateToken


def update_dcl_record(participant_id, new_value, actor_party=None, actor_user=None):
    # create audit record
    DclRecordUpdateToken.objects.create(
        participant_id=participant_id,
        new_value=new_value,
        party=actor_party,
        user=actor_user,
    )
    # perform update
    result = DnsBackend.update_dcl(participant_id, new_value)
    return result


def clear_dcl_record(participant_id, actor_party=None, actor_user=None):
    # create audit record
    DclRecordUpdateToken.objects.create(
        participant_id=participant_id,
        new_value='',
        party=actor_party,
        user=actor_user,
    )
    # perform update
    result = DnsBackend.clear_dcl(participant_id)
    return result
