from django.contrib import admin
from app.models import *


@admin.register(MerchantTransaction)
class MerchantTransactionAdmin(admin.ModelAdmin):
    list_display = ('merchant_id', 'user', 'gateway', 'status')
    list_filter = ('merchant_id', 'user__username', 'gateway', 'status')
    search_fields = ('merchant_id', 'user__username', 'gateway', 'status')
