from member.models import Member
from django.db.models import Sum

def get_individual_deposits():
    return (
        Member.objects
        .annotate(total_deposit=Sum('deposit__deposit_amount'))
        .values(
            'username__first_name', 
            'username__last_name',
            'profile_picture',
            'gender',
            'member_id',
            'community__community_name',
            'total_deposit'
        )
        
    )