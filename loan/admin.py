from django.contrib import admin
from .models import *


# Register your models here.
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'member', 'loan_amount', 'interest_rate', 'tenure', 'status')
    list_filter = ('status', 'member__community', 'application_date')
    

admin.site.register(Loan, LoanAdmin)

class LoanAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'loan_account_number')
    list_filter = ('id', 'loan')

admin.site.register(LoanAccount, LoanAccountAdmin)

class LoanInterestAdmin(admin.ModelAdmin):
    list_display = ('id', 'loan')
    list_filter = ('id', 'loan')

admin.site.register(LoanInterest, LoanInterestAdmin)