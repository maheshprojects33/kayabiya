from django.contrib import admin
from .models import *


# Register your models here.
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'member', 'amount', 'interest_rate', 'tenure', 'status')
    list_filter = ('status', 'application_date')
    

admin.site.register(Loan, LoanAdmin)

