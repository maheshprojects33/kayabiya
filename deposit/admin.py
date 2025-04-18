from django.contrib import admin
from .models import *

# Register your models here.


class DepositAdmin(admin.ModelAdmin):
    list_display = ["date", "account", "deposit_amount", "deposit_by", "remarks"]


admin.site.register(Deposit, DepositAdmin)
