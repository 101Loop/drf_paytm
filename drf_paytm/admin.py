"""
Django admin interfacing of models.

Author: Himanshu Shankar (https://himanshus.com)
"""

from django.contrib import admin

from drfaddons.admin import CreateUpdateAdmin

from .models import PayTMConfiguration, TransactionRequest, TransactionResponse


class PayTMConfigurationAdmin(CreateUpdateAdmin):
    list_display = ('id', 'mid', 'is_active')
    list_display_links = list_display


class TransactionRequestAdmin(CreateUpdateAdmin):
    list_display = ('oid', 'amount', 'mobile', 'email', 'completed',
                    'create_date', 'created_by')

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


class TransactionResponseAdmin(admin.ModelAdmin):
    list_display = ('tid', 'cid', 't_request', 'amount', 'status', 'timestamp')

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.register(PayTMConfiguration, PayTMConfigurationAdmin)
admin.site.register(TransactionRequest, TransactionRequestAdmin)
admin.site.register(TransactionResponse, TransactionResponseAdmin)
