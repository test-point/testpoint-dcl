from __future__ import unicode_literals

import logging

from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView

from dcl_server.backends.route53 import DnsBackend

logger = logging.getLogger(__name__)


class DemoAuthView(APIView):
    """
    Request it and get your auth data echoed back, or 4xx error if something (auth usually) is wrong.
    """

    def get(self, request):
        return Response(
            {
                'user': unicode(request.user),
                'auth': request.auth if isinstance(request.auth, dict) else unicode(request.auth),
                'participant_ids': request.auth.get('participant_ids', []),
                'accredited_parties': request.auth.get('accredited_parties', []),
            }
        )


class HealthcheckView(APIView):
    permission_classes = tuple()

    def get(self, request):
        try:
            get_user_model().objects.count()
        except Exception as e:
            logger.exception(e)
            backend_db = False
        else:
            backend_db = True

        try:
            DnsBackend.get_records(max_items="1")
        except Exception as e:
            logger.exception(e)
            backend_route53 = False
        else:
            backend_route53 = True

        return Response({
            'backend_db': backend_db,
            'backend_route53': backend_route53
        })
