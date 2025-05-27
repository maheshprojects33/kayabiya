from email import message
from urllib import response
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, CreateView, UpdateView
from django.urls import reverse_lazy as _

from .models import Loan
from .forms import *
from member.utils import get_community_head
from member.models import Member

from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.contrib import messages

from account.mixins import StaffRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.
class LoanListView(ListView):
    model = Loan
    template_name = 'loan/loan_list.html'
    context_object_name = 'loans'

class BaseLoanListView(LoginRequiredMixin, ListView):
    model = Loan
    context_object_name = 'loans'

    def get_filtered_queryset(self, statuses=None, exclude_penalty=False, only_penalty=False):
        """
        Helper method to filter loans based on status and penalty conditions.
        """
        queryset = Loan.objects.all()
        user = self.request.user

        # Filter loans based on the provided statuses
        if statuses:
            queryset = queryset.filter(status__in=statuses)

        if exclude_penalty:
            queryset = queryset.exclude(has_penalty="True")

        # Filter loans based on user role
        if user.is_staff:
            # Staff can see all loans
            return queryset
        elif get_community_head(user):
            # If the user is a community head, filter loans for their community members
            queryset = queryset.filter(member__community__community_head=user)
        else:
            # Normal users can only see their own loans
            queryset = queryset.filter(member__username=user.id)

        return queryset
    

class LoanRequestView(BaseLoanListView):
    template_name = 'loan/loan_list_request.html'

    def get_queryset(self):
        # Filter loans based on the status and user role
        # Main code in BaseLoanListView Helper Method
        return self.get_filtered_queryset(statuses=['Pending', 'Approved'])
        

class LoanDisbursedView(BaseLoanListView):
    template_name = 'loan/loan_list_disbursed.html'

    def get_queryset(self):
        # Filter loans based on the status and user role
        # Main code in BaseLoanListView Helper Method
        return self.get_filtered_queryset(statuses=['Disbursed'], exclude_penalty=True)
        

class LoanSettledView(BaseLoanListView):
    template_name = 'loan/loan_list_settled.html'

    def get_queryset(self):
        # Filter loans based on the status
        return self.get_filtered_queryset(statuses=['Settled'])

class LoanVoidedView(BaseLoanListView):
    template_name = 'loan/loan_list_voided.html'

    def get_queryset(self):
        # Filter loans based on the status
        return self.get_filtered_queryset(statuses=['Cancelled', 'Rejected'])

class LoanWatchlistView(BaseLoanListView):
    template_name = 'loan/loan_list_watchlist.html'

    def get_queryset(self):
        # Filter loans based on the status
        return self.get_filtered_queryset(statuses=['Watchlist'])
        return Loan.objects.filter(has_penalty="True")

class LoanApplyView(CreateView):
    model = Loan
    template_name = 'loan/forms/loan_apply.html'
    
    success_url = _('loan_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_form_class(self):
        if self.request.user.is_staff or get_community_head(self.request.user):
            return LoanApplyAdminForm
        else:
            return LoanApplyUserForm
    
    def form_valid(self, form):
        # Only set member for normal users (not staff, not community head)
        if not self.request.user.is_staff and not get_community_head(self.request.user.id):
            form.instance.member = self.request.user.member

        return super().form_valid(form)
    
class LoanUpdateView(UpdateView):
    model = Loan
    template_name = 'loan/forms/loan_update.html'
    form_class = LoanApplyAdminForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Set cancel_url based on sidebar Menu
        if self.object.status == 'Disbursed':
            context['cancel_url'] = _('loan_disbursed')
        elif self.object.status == 'Settled':
            context['cancel_url'] = _('loan_settled')
        elif self.object.status in ['Cancelled', 'Rejected']:
            context['cancel_url'] = _('loan_voided')
        elif self.object.status == 'Watchlist':
            context['cancel_url'] = _('loan_watchlist')
        else:
            context['cancel_url'] = _('loan_request')
        return context

    def get_success_url(self):
        # Redirect to the appropriate loan list based on the status
        if self.object.status == 'Pending' or self.object.status == 'Approved':
            return _('loan_request')
        elif self.object.status == 'Disbursed':
            return _('loan_disbursed')
        elif self.object.status == 'Settled':
            return _('loan_settled')
        elif self.object.status == 'Watchlist':
            return _('loan_watchlist')
        else:
            return _('loan_voided')

    def form_valid(self, form):
        
        # Remove Approved Date if status changed to 'Pending'
        if form.instance.status == 'Pending':
            form.instance.approved_date = None
            form.instance.start_date = None
            form.instance.end_date = None

            form.instance.save(update_fields=['approved_date', 'start_date', 'end_date'])

        # Auto Approved Date if status is Approved
        elif form.instance.status == 'Approved' and not form.instance.approved_date:
            form.instance.approved_date = timezone.now().date()
            form.instance.start_date = None
            form.instance.end_date = None
            form.instance.rejected_reason = None

            form.instance.save(update_fields=['approved_date', 'start_date', 'end_date', 'rejected_reason'])

        # Auto Start Date and End Date if status is Disbursed
        elif form.instance.status == 'Disbursed' and not form.instance.end_date:
            # Check if Loan Status is Approved or not
            if not form.instance.approved_date:
                messages.warning(self.request, "Loan cannot be disbursed without approval.")
                return self.form_invalid(form)
            
            # Set start date to today and calculate end date based on Tenure Months
            form.instance.start_date = timezone.now().date()
            form.instance.end_date = form.instance.start_date + relativedelta(months=form.instance.tenure) - timedelta(days=1)  # Tenure is in months
           
            form.instance.save(update_fields=['start_date', 'end_date'])
        
        elif form.instance.status == 'Disbursed' or form.instance.status == 'Watchlist' and form.instance.end_date:
            if form.instance.has_penalty == True:
                form.instance.status = 'Watchlist'
                form.instance.save(update_fields=['status'])
                
                # Calculation of Penalty
                if form.instance.penalty_type == 'Rate':
                    penalty_amount = form.instance.calculate_penalty(200)
                    print(penalty_amount)
                else:
                    penalty_amount = form.instance.penalty_value
                    print(form.instance.penalty_type, form.instance.penalty_value)
            elif form.instance.status == 'Watchlist' and form.instance.has_penalty == False:
                form.instance.status = 'Watchlist'
                form.instance.save(update_fields=['status'])
            else:
                form.instance.status = 'Disbursed'
                form.instance.save(update_fields=['status'])
    
        # Reason for Rejected and Cancelled Loan
        elif form.instance.status in ['Rejected', 'Cancelled']:
            # If status is Rejected or Cancelled, ensure rejected or cancelled reason is provided
            if not form.instance.rejected_reason:
                messages.error(self.request, "Please provide a reason for Rejection or Cancellation.")
                return self.form_invalid(form)
            
            form.instance.start_date = None
            form.instance.end_date = None

            form.instance.save(update_fields=['rejected_reason', 'start_date', 'end_date'])

        # Auto Settled Date if status is Settled
        elif form.instance.status == 'Settled':
            if not form.instance.start_date or not form.instance.end_date:
                messages.error(self.request, "Loan cannot be settled without Disbursed")
                return self.form_invalid(form)
            form.instance.settled_date = timezone.now().date()
            messages.info(self.request, "Once Loan is settled you can't modifiy anymore are you sure to settle the loan.")
            form.instance.save(update_fields=['settled_date'])

        
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response
    
# class LoanRepaymentView(ListView):
#     model = Loan
#     template_name = 'loan/loaner_list.html'
#     context_object_name = 'loans'

#     def get_queryset(self):
#         # Filter loans based on the status
#         return Loan.objects.filter(status__in = ['Disbursed', 'Watchlist'])
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['repayment_type'] = Loan.REPAYMENT_TYPE
    #     return context