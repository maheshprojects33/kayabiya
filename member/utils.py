import re
import trace
from member.models import Member, Community
from django.db.models import Sum

def get_individual_deposits():
    return (
        Member.objects
        .annotate(total_deposit=Sum('deposit__deposit_amount' or 0))
        .values(
            'username__first_name', 
            'username__last_name',
            'profile_picture',
            'gender',
            'member_id',
            'community__community_name',
            'total_deposit'
        ).exclude(total_deposit = 0)
        
    )

def get_individual_loans():
    return (
        Member.objects.filter(loans__status='Disbursed' or 0)
            .annotate(total_loan=Sum('loans__loan_amount'))
            .values(
                'username__first_name', 
                'username__last_name',
                'profile_picture',
                'gender',
                'member_id',
                'community__community_name',
                'total_loan'
        )
        
    )

def get_community_head(login_user):
    is_community_head = Community.objects.filter(community_head=login_user)
    return is_community_head

# Function to record a transaction History

recent_transaction = []

def record_transaction(description, community, date, time, amount, remarks=None):
    transaction = {
        'description': description,
        'community': community,
        'date': date,
        'time': time,
        'amount': amount,
        'remarks': remarks
    }
    recent_transaction.append(transaction)
    return recent_transaction

def get_recent_transactions():
    return sorted(
        recent_transaction,
        key=lambda x: (x['date'], x['time']),
        reverse=True
    )

  