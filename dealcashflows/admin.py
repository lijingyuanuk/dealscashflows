
from collections import OrderedDict

from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site
from django.utils.text import capfirst

from models import *


admin.site.unregister(Group)
admin.site.unregister(Site)
admin.site.unregister(User)

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'local_currency', 'fund']


@admin.register(Cashflow)
class CashflowAdmin(admin.ModelAdmin):
    list_display = ['id', 'deal', 'value_date', 'cf_type', 'cashflows']

