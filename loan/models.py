from django.db import models
from member.models import Member
from django.utils import timezone
from datetime import timedelta
import calendar
from decimal import Decimal
import re


from django.db.models import Sum

# Create your models here.
class Loan(models.Model):
    PENALTY_TYPE = [
        ('Fixed', 'Fixed Amount'),
        ('Rate', 'Percentage Rate'),
    ]
    LOAN_STATUS = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Disbursed', 'Disbursed'),
        ('Rejected', 'Rejected'),
        ('Settled', 'Settled'),
        ('Cancelled', 'Cancelled'),
        ('Watchlist', 'Watchlist'),
    ]
    REPAYMENT_TYPE = [
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Yearly', 'Yearly'),
    ]
    

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='loans')
    loan_amount = models.DecimalField(max_digits=9, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)  # e.g., 5.25%
    tenure = models.PositiveIntegerField(default=12)  # Duration in months
    
    application_date = models.DateField(auto_now_add=True) # Auto-generated date when the loan application is created
    approved_date = models.DateField(blank=True, null=True) # Auto-generated date when the loan is approved
    start_date = models.DateField(blank=True, null=True) # Auto-generated date when the loan is disbursed
    end_date = models.DateField(blank=True, null=True) # Auto-generated date when the loan is disbursed
    settled_date = models.DateField(blank=True, null=True)  # Auto-generated date when the loan is settled

    collateral = models.TextField(blank=True, null=True)
    collateral_proof = models.FileField(upload_to='collateral_proofs/', blank=True, null=True)
    guarantor = models.CharField(max_length=50, blank=True, null=True)

    purpose = models.CharField(max_length=255)

    repayment_type = models.CharField(max_length=9, choices=REPAYMENT_TYPE, default='Monthly')

    # Penalty fields
    has_penalty = models.BooleanField(default=False)
    penalty_type = models.CharField(max_length=5, choices=PENALTY_TYPE, default='Rate')
    penalty_value = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    status = models.CharField(max_length=9, choices=LOAN_STATUS, default='Pending')
    rejected_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Loan {self.id} - {self.member.username}"
    
    def calculate_penalty(self, base_amount):
        if self.penalty_type == 'Rate':
            print(base_amount, self.penalty_value, "Model Bata")
            return base_amount * (self.loan_amount / 100)
        return self.penalty_value
    
    @property # This property calculates the days to expiry based on the end date READ-ONLY Property
    def days_to_expiryProperty(self):
        if self.end_date:
            today = timezone.now().date()
            return (self.end_date - today).days
        return None
    

class LoanAccount(models.Model):
    loan_account_number = models.CharField(max_length=20, unique=True) # Auto-generated loan account number

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='loan_accounts')
    interest_per_day = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    interest_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    interest_paid = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Account {self.loan_account_number} - Loan {self.loan.id}"
    

    @staticmethod # Static method to get the next account number based on the existing accounts
    def get_next_account_number(accounts_queryset, prefix):
        max_number = 0
        for acc in accounts_queryset:
            match = re.search(r'(\d+)$', acc.loan_account_number)
            if match:
                num = int(match.group())
                if num > max_number:
                    max_number = num
        new_numeric_part = max_number + 1 if max_number else 1
        return f"{prefix}-{new_numeric_part:03d}"


    # auto-generated loan account number
    def save(self, *args, **kwargs):
        if not self.loan_account_number:
            # get member community and generate a unique account number
            # Format: Initial of Each Words of Community + Communit ID + S.No. starting from 001
            community = self.loan.member.community
            print(community, "Community")
            
            if community:
                community_initials = ''.join(word[0].upper() for word in community.community_name.split()) # Get initials of community name
                community_id = community.id 
                print(community_initials, community_id, "Community Initials and ID")
            else:
                community_initials = 'NA'
                community_id = '00'
            unique_number_filter = f"{community_initials}-{community_id:02d}" 
            unique_number = f"{community_initials}-{community_id:02d}-001"  # Format: CDCS-01-001
            

            # Get all accounts for this community
            existing_accounts = LoanAccount.objects.filter(loan_account_number__startswith=unique_number_filter)
            
            if existing_accounts.exists():
                self.loan_account_number = self.get_next_account_number(existing_accounts, unique_number_filter)
            else:
                self.loan_account_number = unique_number

        if not self.pk:
            self.interest_per_day = self.accrued_interest
        super().save(*args, **kwargs)
    
  
    @property
    # To Calculate Accrued Interest
    def accrued_interest(self):
        loan = self.loan
        current_day = timezone.now().date()
        disbursed_date = loan.start_date
        end_date = loan.end_date
        loan_amount = loan.loan_amount
        interest_rate = loan.interest_rate

        # Covertion of non Decimal Values to Decimal for calculation 
        days = (current_day + timedelta(days=1) - disbursed_date).days
        converted_interest_rate = interest_rate / Decimal('100')
        calulated_days = Decimal(days) / Decimal('365')

        if current_day > end_date:
            # Optionally handle fine or overdue logic here
            return Decimal('0.00')
        else:
            # loan_account = LoanInterest.objects.filter(loan=loan)
            # print(loan_account)

            interest_amount = loan_amount * converted_interest_rate * calulated_days
            
            return interest_amount.quantize(Decimal('0.01'))
        
    @property
    # To Calculate Monthly Interest base on the days of current Month
    def monthly_interest(self):
        today = timezone.now().date()
        days_in_month = calendar.monthrange(today.year, today.month)[1]
        print(days_in_month, "x", self.interest_per_day, "=", days_in_month*self.interest_per_day )
        monthly_interest_amount = self.interest_per_day * days_in_month
        return monthly_interest_amount.quantize(Decimal('0.01'))

class LoanInterest(models.Model):
    MONTH_CHOICES = [
    (1, 'January'),
    (2, 'February'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December'),
]

    loan = models.ForeignKey(LoanAccount, on_delete=models.CASCADE, related_name='loan_interest')
    interest_amount = models.DecimalField(max_digits=9, decimal_places=2)
    month = models.IntegerField(choices=MONTH_CHOICES, blank=True, null=True)
    paid_amount = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)
    



    