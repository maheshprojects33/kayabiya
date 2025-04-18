from datetime import datetime
from django.db import models

from member.models import Member

# Create your models here.
class Deposit(models.Model):
    date = models.DateField(default=datetime.now)
    account = models.ForeignKey(Member, on_delete=models.CASCADE)
    deposit_amount = models.PositiveIntegerField()
    deposit_by = models.CharField(max_length=50, default="Self")
    remarks = models.CharField(max_length=100, blank=True, null=True)
