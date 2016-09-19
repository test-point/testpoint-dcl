import pprint  # NOQA

from django.core.management.base import BaseCommand


from dcl_server.backends.route53 import DnsBackend


class Command(BaseCommand):
    help = 'Play with NAPTR client'

    def handle(self, *args, **options):
        result = DnsBackend.get_records()
        # pprint.pprint(result)
        for r in result['ResourceRecordSets']:
            if r['Type'] == 'NAPTR':
                pprint.pprint(r)
        # self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))

        # DnsBackend.update_dcl(
        #     "urn:oasis:names:tc:ebcore:partyid-type:iso6523:0151::17624904938",
        #     "wow.smp.testpoint.io"
        # )
        return
