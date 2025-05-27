from math import log
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from member.models import Member, Community
from deposit.models import Deposit

from django.db.models import Sum
from member.utils import get_individual_deposits, get_community_head


# Create your views here.
class Dashboard(LoginRequiredMixin, ListView):
    model = Member 
    template_name = 'dashboard/dashboard.html'

    def get_template_names(self):
        login_user = self.request.user
        # is_community_head = Community.objects.filter(community_head=login_user)
        

        if login_user.is_staff:
            return ['dashboard/dashboard-admin.html']
        elif get_community_head(login_user):
            return ['dashboard/dashboard-head.html']
        else:
            return ['dashboard/dashboard-member.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        login_user = self.request.user
        is_community_head = get_community_head(login_user)

        

        # For Member Dashboard
        if not login_user.is_staff and not is_community_head:
            member_community = login_user.member.community
            context["member_community"] = member_community
            context["member_community_head"] = member_community.community_head.all()

        # For Admin Dashboard
        context ["total_members"] = Member.objects.count()
        context ["total_communities"] = Community.objects.count()

        # Total Members of Individual Community (Head Dashboard)
        context["total_community_members"] = Member.objects.filter(community__community_head=login_user).count()
        context["head"] = is_community_head.first()

        Total_Deposit = Deposit.objects.all()
        context ["total_deposit"] = Total_Deposit.aggregate(Sum('deposit_amount'))['deposit_amount__sum'] or 0

        # Total deposit by All community (Admin Dashboard)
        community_deposits = (
        Community.objects
        .annotate(total_deposit=Sum('community_members__deposit__deposit_amount'))
        .values('community_name', 'total_deposit')
        )
        context["community_total_deposit"] = community_deposits

        # Individual total deposit of all Members (Admin Dashboard) #Code is in utils.py in member app
        individual_deposits = get_individual_deposits().order_by('-total_deposit')
        
        context["individual_total_deposit"] = individual_deposits[:10]

        # Login Member Total Deposit (Member Dashboard)
        context["member_total_deposit"] = individual_deposits.filter(username__first_name=login_user.first_name).first()

        # Total Deposit of Individual Community (Head Dashboard)
        communityHead_total_deposits = individual_deposits.filter(community__community_name=is_community_head.first())
        communityHead_total_deposit = communityHead_total_deposits.aggregate(Sum('total_deposit'))['total_deposit__sum'] or 0
        context["communityHead_total_deposit"] = communityHead_total_deposit
        
        context["communityHead_members_deposit"] = communityHead_total_deposits[:10]


        return context

    
    