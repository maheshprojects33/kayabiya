from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone

    
    

class Community(models.Model):
    community_name = models.CharField(max_length=255)
    community_head = models.ManyToManyField(User, related_name='managed_community')

    def __str__(self):
        return self.community_name
    


class Member(models.Model):
    MARITAL_STATUS = [
        ('Single', 'Single'),
        ('Married', 'Married'),
    ]
    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    STATUS = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    MEMBER_TYPE = [
        ('General', 'General'),
        ('Executive', 'Executive'),
    ]
    ROLE_CHOICES = [
        ('Member', 'Member'),
        ('Community-Head', 'Community-Head'),
        ('Executive', 'Executive'),
    ]
    
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, blank=True, null=True, related_name='community_members')
    gender = models.CharField(max_length=6, choices=GENDER, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    marital_status = models.CharField(
        max_length=7, choices=MARITAL_STATUS, null=True, blank=True
    )
    mobile = models.CharField(max_length=10, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    ward = models.CharField(max_length=3, null=True, blank=True)
    house_number = models.CharField(max_length=10, blank=True)
    citizenship_number = models.CharField(max_length=10, blank=True)
    join_date = models.DateField(null=True, blank=True)
    member_type = models.CharField(max_length=9, choices=MEMBER_TYPE, default="General")
    profile_picture = models.ImageField(upload_to="profile/", blank=True, null=True)
    citizen_copy = models.ImageField(upload_to="citizen/", blank=True, null=True)
    status = models.CharField(max_length=8, choices=STATUS, default="Active")
    # Auto Generated Fields
    age = models.IntegerField(null=True, blank=True)
    member_id = models.CharField(max_length=6, unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Calculation of Age
        if self.dob:
            current_date = timezone.now().date()
            self.age = current_date.year - self.dob.year
        else:
            pass

        # Member ID Generation
        if not self.member_id:
            last_member = Member.objects.all().order_by('id').last()
            if last_member:
                last_member_id = int(last_member.member_id)
                self.member_id = f'{last_member_id + 1:03d}'
            else:
                self.member_id = "001"

        super().save(*args, **kwargs)

    
    def __str__(self):
        return str(self.username.get_full_name())
    