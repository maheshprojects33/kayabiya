from member.models import Member, Community
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

def get_community_head(login_user):
    is_community_head = Community.objects.filter(community_head=login_user)
    return is_community_head