from django.contrib import admin

from .models import DclRecordUpdateToken


@admin.register(DclRecordUpdateToken)
class DclRecordUpdateTokenAdmin(admin.ModelAdmin):
    search_fields = ('participant_id', 'new_value')
    list_display = ('participant_id', 'new_value', 'party', 'user', 'created')
