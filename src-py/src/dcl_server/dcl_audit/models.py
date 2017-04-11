from __future__ import unicode_literals

from django.conf import settings
from django.db import models


class DclRecordUpdateToken(models.Model):
    participant_id = models.CharField(max_length=2048)
    new_value = models.TextField(max_length=5 * 1024, blank=True, default='')

    party = models.ForeignKey('accreditations.AccreditedParty', blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        help_text='Staff member who performed the action, if applicable',
        blank=True, null=True
    )

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return "DCL Update for {} to {}".format(self.participant_id, self.new_value)
