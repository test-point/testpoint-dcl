import logging
import pprint  # NOQA

import boto3
from constance import config
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from dcl_server.oasis.utils import get_hash

from .exceptions import DclBackendValidationError

logger = logging.getLogger(__name__)


class DnsBackend(object):
    """
    Route53 dns backend, sends queries to AWS Route53 service and updates NAPTR
    records there
    http://boto3.readthedocs.io/en/stable/reference/services/route53.html

    Test case:
        * get current value for your Participant Id
        * update the value
        * wait some time
        * check new value using your AWS DNS Server
        * check new value from another host after some timeout (1, 5, 10, 60 minutes - it depends)

    In case of any problems:
        * check for useful logging output
        * check if record has been updated in Route53 console

    To test random record:
        $ host -t naptr b-a8bed6634b24fe2ae8045bf3ded8e2f0.dcl.testpoint.io. ns-1541.awsdns-00.co.uk
        b-a8bed6634b24fe2ae8045bf3ded8e2f0.dcl.testpoint.io has NAPTR record 10 100 "S" "" "" dcp.testpoint.io.

    """

    @staticmethod
    def _get_client():
        return boto3.client(
            'route53',
            aws_access_key_id=settings.ROUTE_53_IAM_ACCESS_KEY,
            aws_secret_access_key=settings.ROUTE_53_IAM_ACCESS_SECRET,
        )

    @staticmethod
    def get_records(max_items=None):
        """
        Return extensive dict with records info; pprint it to get the format
        """
        client = DnsBackend._get_client()
        response = client.list_resource_record_sets(
            HostedZoneId=settings.ROUTE53_ZONE_ID,
            MaxItems=max_items
        )
        return response

    @staticmethod
    def prepare_domain_name(new_smp_domain):
        """
        Ensure that domain name has correct format and characters set
        """
        if '"' in new_smp_domain or "'" in new_smp_domain:
            # sentry will have local variables for debug
            raise DclBackendValidationError("Wrong characters found in domain name")
        return new_smp_domain

    @staticmethod
    def update_dcl(participant_id, new_smp_hostname):
        """
        Update record for the given participant.
        Parameters:
            * participant_id: '{scheme}::{value}'
              example: "urn:oasis:names:tc:ebcore:partyid-type:iso6523:0151::60887492061"
            * new_smp_hostname: domain of Service Metadata Publisher host
              example: dcp.testpoint.io, stage.dcp.testpoint.io
        Return value: unspecificed
        Raises:
            * DclBackendValidationError if input data is wrong, but generally assumes that
              data should be checked before calling this procedure.
            * DclBackendPushException when it's impossible to save the data to AWS
        """
        if settings.ROUTE53_ZONE_ID is None:
            raise ImproperlyConfigured(
                "settings.ROUTE53_ZONE_ID must be set to use route53 backend"
            )
        validated_smp_hostname = DnsBackend.prepare_domain_name(new_smp_hostname)

        client = DnsBackend._get_client()
        new_record_name = "B-{}.{}.".format(
            get_hash(participant_id),
            settings.DCL_DNS_HOSTNAME
        )

        new_record_value = u'{record_prefix} {new_domain_name}.'.format(
            record_prefix=settings.DCL_RECORD_PREFIX,
            new_domain_name=validated_smp_hostname
        )
        logger.info(u"New NAPTR record for %s is %s", new_record_name, new_record_value)

        response = client.change_resource_record_sets(
            HostedZoneId=settings.ROUTE53_ZONE_ID,
            ChangeBatch={
                'Comment': 'Update NAPTR record for specific domain',
                'Changes': [
                    {
                        'Action': "UPSERT",
                        'ResourceRecordSet': {
                            'Name': new_record_name.lower(),
                            'Type': 'NAPTR',
                            'TTL': config.DCL_NAPTR_RECORD_TTL,
                            'ResourceRecords': [
                                {
                                    'Value': new_record_value.lower()
                                }
                            ],
                        }
                    },
                ]
            }
        )
        # TODO: it's quite verbose; may be removed after proper response handling.
        logger.info(response)
        return

    @staticmethod
    def clear_dcl(participant_id):
        """
        Delete record for given participant if it exists
        """
        if settings.ROUTE53_ZONE_ID is None:
            raise ImproperlyConfigured(
                "settings.ROUTE53_ZONE_ID must be set to use route53 backend"
            )
        client = DnsBackend._get_client()
        record_name = "b-{}.{}.".format(
            get_hash(participant_id),
            settings.DCL_DNS_HOSTNAME
        ).lower()

        existing_record_set_resp = client.list_resource_record_sets(
            HostedZoneId=settings.ROUTE53_ZONE_ID,
            StartRecordName=record_name,
            MaxItems="1"
        )
        # pprint.pprint(existing_record_set_resp)
        record_set = None
        if len(existing_record_set_resp) == 0:
            record_set = None
        else:
            rs = existing_record_set_resp['ResourceRecordSets'][0]
            if rs['Name'] == record_name:
                record_set = existing_record_set_resp['ResourceRecordSets'][0]
            else:
                pass
        if record_set is None:
            logger.error(
                "Tried to delete record set for %s %s but it wasn't found",
                participant_id,
                record_name
            )
            return False

        # pprint.pprint(record_set)

        try:
            response = client.change_resource_record_sets(
                HostedZoneId=settings.ROUTE53_ZONE_ID,
                ChangeBatch={
                    'Comment': 'Drop NAPTR record for specific domain',
                    'Changes': [
                        {
                            'Action': "DELETE",
                            'ResourceRecordSet': record_set
                        },
                    ]
                }
            )
        except Exception as e:
            logger.exception(e)
            return False
        # TODO: it's quite verbose; may be removed after proper response handling.
        logger.info(response)
        return True
