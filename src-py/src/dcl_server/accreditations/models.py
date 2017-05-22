from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils import timezone


class AccreditedParty(models.Model):
    TYPE_DCP = 'dcp'

    TYPES_CHOICES = (
        (TYPE_DCP, 'DCP'),
    )

    STATUS_ACCR = 'acrdt'
    STATUS_PEND = 'pend'
    STATUS_SUSP = 'susp'
    STATUS_REVO = 'rev'
    STATUS_CANC = 'can'

    STATUS_CHOICES = (
        (STATUS_ACCR, 'Accredited'),
        (STATUS_PEND, 'Pending'),
        (STATUS_SUSP, 'Suspended'),
        (STATUS_REVO, 'Revoked'),
        (STATUS_CANC, 'Cancelled'),
    )

    # if we have participant_id here then we can assume any trusted JWT with that
    # participant_id as a valid JWT from this party,
    # and let it change records for any participant ID (audited)
    service_provider_id = models.CharField(
        "Service Provider ID",
        max_length=1024,
        unique=True,
    )
    trading_name = models.CharField(
        "Trading Name",
        max_length=1024,
        unique=True,
    )
    contact_email = models.CharField(
        "Contact Email",
        max_length=1024
    )
    registration_url = models.CharField(
        "URL (for registration page)",
        max_length=2048,
    )
    dcp_host = models.CharField(
        max_length=2048,
        default='dcp-for-this-party.testpoint.io',
        unique=True,
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    party_type = models.CharField(max_length=10, choices=TYPES_CHOICES, default=TYPE_DCP)
    accreditation_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES, default=STATUS_PEND
    )

    class Meta:
        verbose_name = 'accredited party'
        verbose_name_plural = 'accredited parties'
        ordering = ('-created',)

    def __unicode__(self):
        return "DCP {}".format(self.service_provider_id)

    @property
    def valid_certificates(self):
        now = timezone.now()
        return {
            'client': list(self.certs.filter(
                models.Q(revoked__gt=now) | models.Q(revoked__isnull=True),
                is_client=True,
            ).values_list('body', flat=True)),
            'server': list(self.certs.filter(
                models.Q(revoked__gt=now) | models.Q(revoked__isnull=True),
                is_client=False,
            ).values_list('body', flat=True)),
        }


class PartyCertificate(models.Model):
    party = models.ForeignKey(AccreditedParty, related_name='certs')
    body = models.TextField("Certificate", blank=True)
    is_client = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    revoked = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return "Certificate for {}".format(self.party)


class PartyFieldUpdate(models.Model):
    party = models.ForeignKey(AccreditedParty)
    field = models.CharField(max_length=200)
    new_value = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        help_text='Staff member who performed the action',
        blank=True, null=True
    )

    class Meta:
        ordering = ('-id',)

    def __unicode__(self):
        return "User {} changes party {} field {} to {}".format(
            self.actor,
            self.party,
            self.field,
            self.new_value
        )


class PartyAccreditationChangeEvent(models.Model):
    # This form will capture critical information to support the revocation
    # decision and provide an enduring audit record.
    party = models.ForeignKey(AccreditedParty)
    old_status = models.CharField(
        max_length=20,
        choices=AccreditedParty.STATUS_CHOICES
    )
    new_status = models.CharField(
        max_length=20,
        choices=AccreditedParty.STATUS_CHOICES
    )

    freetext_reason = models.TextField(
        help_text='Free text explanation why party accreditation has been changed',
        blank=True, default=''
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        help_text='Staff member who performed the action',
        blank=True, null=True
    )

    created = models.DateTimeField(
        help_text="Moment of time when the action was performed",
        auto_now_add=True
    )

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return "ChangeEvent #{} for {}".format(self.id, self.party)


class UserPartyAccess(models.Model):
    """
    Once user has been authenticated in our system some Django user record
    is created; and we can give access to this user to some Party manually.
    Agnostic to auth method (TLS, JWT or even Django users directly - doesn't matter)
    """

    party = models.ForeignKey(AccreditedParty)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        unique_together = ('party', 'user')

    def __unicode__(self):
        ret = "User {} access to {}".format(self.user, self.party)
        if not self.is_active:
            ret += " (inactive)"
        return ret
