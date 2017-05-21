from __future__ import unicode_literals

from django import forms
from django.contrib import admin

from .models import (
    AccreditedParty, PartyCertificate, PartyAccreditationChangeEvent,
    UserPartyAccess, PartyFieldUpdate
)


class AccreditedPartyForm(forms.ModelForm):

    def save(self, *args, **kwargs):
        if self.instance and self.instance.pk:
            model_before_save = AccreditedParty.objects.get(pk=self.instance.pk)
        else:
            model_before_save = None
        saved_instance = super(AccreditedPartyForm, self).save(*args, **kwargs)
        if model_before_save:
            for field in self.fields:
                old_value = getattr(model_before_save, field, None)
                new_value = getattr(saved_instance, field, None)
                if old_value != new_value:
                    PartyFieldUpdate.objects.create(
                        actor=self.user,
                        field=field,
                        party=saved_instance,
                        new_value=new_value,
                    )
        return saved_instance


@admin.register(AccreditedParty)
class AccreditedPartyAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'service_provider_id', 'trading_name', 'party_type', 'accreditation_status', 'created'
    )
    list_filter = ('party_type', 'accreditation_status')
    search_fields = (
        'service_provider_id', 'trading_name', 'contact_email', 'registration_url'
    )
    form = AccreditedPartyForm

    def get_form(self, request, instance, *args, **kwargs):
        form_instance = super(AccreditedPartyAdmin, self).get_form(request, instance, *args, **kwargs)
        form_instance.user = request.user
        return form_instance


@admin.register(PartyCertificate)
class PartyCertificateAdmin(admin.ModelAdmin):
    list_filter = ('is_client',)
    list_display = ('party', 'is_client', 'created', 'updated', 'revoked')


@admin.register(PartyAccreditationChangeEvent)
class PartyAccreditationChangeEventAdmin(admin.ModelAdmin):
    list_display = (
        'party', 'old_status', 'new_status', 'actor'
    )

    def has_delete_permission(self, *args, **kwargs):
        return False


@admin.register(UserPartyAccess)
class UserPartyAccessAdmin(admin.ModelAdmin):
    list_display = ('party', 'user', 'is_active', 'created')


@admin.register(PartyFieldUpdate)
class PartyFieldUpdateAdmin(admin.ModelAdmin):
    search_fields = ('field', 'new_value')
    list_display = ('actor', 'party', 'field', 'new_value', 'created')

    def has_delete_permission(self, *args, **kwargs):
        return False
