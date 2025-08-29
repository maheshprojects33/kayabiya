from django import forms
from .models import *
from member.models import Member


class LoanApplyUserForm(forms.ModelForm):
    class Meta:
        model = Loan
        
        fields = [
            
            "loan_amount",
            "purpose",
            "tenure",
            "repayment_type",
            "guarantor",
            "collateral",
            "collateral_proof",
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

class LoanApplyAdminForm(forms.ModelForm):
    class Meta:
        model = Loan
        
        fields = "__all__"
        exclude = ["days_to_expiry", "approved_date", "start_date", "end_date", "settled_date"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)
        
        instance = self.instance # To check the instance status
        print(instance.status)
        

        # Limit the status choices based on the current instance status
        if instance.status == 'Pending':
            self.fields['status'].choices = [
                ('Pending', 'Pending'),
                ('Approved', 'Approved'),
                ('Rejected', 'Rejected'),
                ('Cancelled', 'Cancelled'),
            ]   
        elif instance.status == 'Approved':
            self.fields['status'].choices = [
                ('Approved', 'Approved'),
                ('Disbursed', 'Disbursed'),
                ('Rejected', 'Rejected'),
                ('Cancelled', 'Cancelled'),
            ]   
        elif instance.status == 'Disbursed':
            self.fields['status'].choices = [
                ('Disbursed', 'Disbursed'),
                ('Settled', 'Settled'),
                ('Watchlist', 'Watchlist'),
            ]
            # Disable all fields except the listed fields
            for name, field in self.fields.items():
                if name not in ['status', 'has_penalty', 'penalty_type', 'penalty_value']:
                    field.disabled = True
        elif instance.status in ['Rejected', 'Cancelled']:
            self.fields['status'].choices = [
                ('Rejected', 'Rejected'),
                ('Cancelled', 'Cancelled'),
                ('Pending', 'Pending'),
            ]
            # Disable all fields except 'status' and 'rejected_reason'
            for name, field in self.fields.items():
                if name not in ['status', 'rejected_reason']:
                    field.disabled = True
        elif instance.status == 'Settled':
            # Disable all fields 
            for field in self.fields.values():
                field.disabled = True  
        elif instance.status == 'Watchlist':
            self.fields['status'].choices = [
                ('Watchlist', 'Watchlist'),
                ('Disbursed', 'Disbursed'),
                ('Settled', 'Settled'),
            ]
            # Disable all fields except the listed fields
            for name, field in self.fields.items():
                if name not in ['status', 'has_penalty', 'penalty_type', 'penalty_value']:
                    field.disabled = True
        
        # To update all fields with the form-control class
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
        self.fields['has_penalty'].widget.attrs.update({'class': 'form-check-input'})

        # Filter the member queryset based on user role
        # Check if 'member' field is in the form and user is passed or None
        if 'member' in self.fields and user:
            self.fields['member'].queryset = Member.objects.all()
        
        # Filter the member queryset based on user role
        # If user is community head, show only members of their communities
            if user.is_staff:
                self.fields['member'].queryset = Member.objects.all()
            elif hasattr(user, 'managed_community'):
                communities = user.managed_community.all()
                self.fields['member'].queryset = Member.objects.filter(community__in=communities)
            else:
                self.fields['member'].queryset = Member.objects.none()

        
class LoanAccountForm(forms.ModelForm):
    class Meta:
        model = LoanAccount
        fields = "__all__"
        exclude = ["loan_account_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

class LoanInterestForm(forms.ModelForm):
    class Meta:
        model = LoanInterest
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

        # Disable all fields except 'Paid Amount'
        for name, field in self.fields.items():
            if name not in ['paid_amount']:
                field.disabled = True