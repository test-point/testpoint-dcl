import pprint  # NOQA

from django.core.management.base import BaseCommand


from dcl_server.backends.route53 import DnsBackend


class Command(BaseCommand):
    help = 'Play with NAPTR client'

    def handle(self, *args, **options):
        result = DnsBackend.get_records()
        for r in result['ResourceRecordSets']:
            if r['Type'] == 'NAPTR':
                pprint.pprint(r)
        return
