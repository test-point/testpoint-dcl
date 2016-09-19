# from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView
from django.shortcuts import redirect

from dcl_server.backends.route53 import DnsBackend
from dcl_server.oasis.constants import PID_ABN, OASIS_PREFIX_ABN
from dcl_server.oasis.utils import get_hash


class ParticipantRequiredMixin(object):
    participant_id = None

    def dispatch(self, request, *args, **kwargs):
        """
        Return super().dispatch result if current request have session with some ABN
        or error message and redirect to index page if not
        """
        if not request.user.is_authenticated():
            messages.warning(request, 'Please authenticate first')
            return redirect('/')
        abn_provided = request.session.get('userinfo', {}).get(PID_ABN)
        if not abn_provided:
            messages.warning(request, 'No ABN provided for this user - please use idp.testpoint.io with correct user')
            return redirect('/')
        try:
            int(abn_provided)
        except (ValueError, TypeError):
            messages.error(request, 'Wrong ABN {} provided'.format(abn_provided))
            return redirect('/')
        self.participant_id = u'{}::{}'.format(
            OASIS_PREFIX_ABN,
            abn_provided
        )
        return super(ParticipantRequiredMixin, self).dispatch(request, *args, **kwargs)


class IndexUiView(ParticipantRequiredMixin, TemplateView):
    template_name = 'ui/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IndexUiView, self).get_context_data(*args, **kwargs)
        context.update({
            'participant_id': self.participant_id,
            'participant_hash': get_hash(self.participant_id)
        })
        return context

    def post(self, request, *args, **kwargs):
        # for key in request.session.keys():
        #     print(key, request.session.get(key))
        new_smp_value = request.POST.get('new_smp_value', '')
        if new_smp_value:
            new_smp_value = new_smp_value.strip()
            DnsBackend.update_dcl(self.participant_id, new_smp_value)
            messages.success(request, 'Value update scheduled')
        return redirect(request.path_info)
