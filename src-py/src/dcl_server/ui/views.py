# from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView
from django.shortcuts import redirect

from dcl_server.backends.generic import update_dcl_record, clear_dcl_record
from dcl_server.oasis.utils import get_hash
from dcl_server.dcl_api_v0.authentication import get_participant_ids_for_auth
from dcl_server.dcl_audit.models import DclRecordUpdateToken


class ParticipantRequiredMixin(object):
    participant_id = None
    participant_ids = []

    def dispatch(self, request, *args, **kwargs):
        """
        Return super().dispatch result if current request have session with some ABN
        or error message and redirect to index page if not
        """
        if not request.user.is_authenticated():
            messages.warning(request, 'Please authenticate first')
            return redirect('/')
        self.participant_ids = get_participant_ids_for_auth(
            request.session.get('userinfo', {})
        )
        return super(ParticipantRequiredMixin, self).dispatch(request, *args, **kwargs)


class IndexUiView(ParticipantRequiredMixin, TemplateView):
    template_name = 'ui/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IndexUiView, self).get_context_data(*args, **kwargs)
        context.update({
            'participant_id': self.participant_ids[0] if self.participant_ids else None,
            'participant_ids': self.participant_ids,
            'participant_hash': get_hash(
                self.participant_ids[0]
            ) if self.participant_ids else "{your-participant-hash-here}",
            'update_history': DclRecordUpdateToken.objects.filter(
                participant_id__in=self.participant_ids
            )[:50]
        })
        return context

    def post(self, request, *args, **kwargs):
        if self.participant_ids:
            participant_id = request.POST.get('participant_id', '')
            if participant_id not in self.participant_ids:
                messages.error(
                    request,
                    "Strange error with participant id; make sure you have correct"
                    "participant IDs in your auth and you don't pass any PID which "
                    "you don't own"
                )
                return redirect(request.path_info)

            new_dcp_value = request.POST.get('new_dcp_value', '').strip()
            if new_dcp_value:
                update_dcl_record(participant_id, new_dcp_value)
                messages.success(request, 'The value update has been scheduled')
            else:
                result = clear_dcl_record(participant_id)
                if result is True:
                    messages.success(request, 'The value removal has been scheduled')
                else:
                    messages.warning(
                        request,
                        "The value removal has failed; may be you didn't have DCL "
                        "record for this Participant ID"
                    )
        return redirect(request.path_info)
