from django.db import models
from member.models import Member
from django.utils import timezone

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
    amount = models.DecimalField(max_digits=9, decimal_places=2)
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
            return base_amount * (self.amount / 100)
        return self.penalty_value
    
    @property # This property calculates the days to expiry based on the end date READ-ONLY Property
    def days_to_expiryProperty(self):
        if self.end_date:
            today = timezone.now().date()
            return (self.end_date - today).days
        return None
    

    


