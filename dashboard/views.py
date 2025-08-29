from math import log
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from member.models import Member, Community
from deposit.models import Deposit
from loan.models import Loan

from django.db.models import Sum, Q
from member.utils import *




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

        '''
        Admin Dashboard:
        '''
        # For Admin Dashboard (Admin Dashboard First Row)
        context ["total_members"] = Member.objects.count()
        context ["total_communities"] = Community.objects.count()
        context ["total_deposit"] = Deposit.objects.all().aggregate(Sum('deposit_amount'))['deposit_amount__sum'] or 0
        context["total_loans"] = Loan.objects.filter(status='Disbursed').aggregate(Sum('loan_amount'))['loan_amount__sum'] or 0

        # Total deposit by Individual community (Admin Dashboard Ref Second Row)
        community_deposits = (
            Community.objects.annotate(
                total_deposit=Sum('community_members__deposit__deposit_amount')).values(
                    'community_name', 'total_deposit')
            )
        
        # context["community_total_deposit"] = community_deposits

        # Total Loan by Individual community (Admin Dashboard Ref Second Row)
        community_loans = Loan.objects.filter(status='Disbursed').values(
            'member__community__community_name').annotate(total_loan=Sum('loan_amount'))
        # context["community_total_loan"] = community_loans

        # Combine total deposit and total loan per community (Admin Dashboard Second Row)
        # Build lookup dictionaries
        deposit_dict = {c['community_name']: c['total_deposit'] or 0 for c in community_deposits}
        loan_dict = {c['member__community__community_name']: c['total_loan'] or 0 for c in community_loans}

        # Merge both dictionaries into a list of dictionaries (Admin Dashboard Second Row)
        community_stats = []
        for community_name in deposit_dict:
            community_stats.append({
                'community_name': community_name,
                'total_deposit': deposit_dict.get(community_name, 0),
                'total_loan': loan_dict.get(community_name, 0) #Since both deposit and loan have same number of community and community_name it is safe for literation
            })

        context["community_stats"] = community_stats

        # Individual total deposit of all Members (Admin Dashboard Third Row) #Code is in utils.py in member app
        individual_deposits = get_individual_deposits().order_by('-total_deposit')
        individual_loans = get_individual_loans().order_by('-total_loan')
        
        context["individual_total_deposit"] = individual_deposits[:10]
        context["individual_total_loan"] = individual_loans[:10]

        '''
        Community-Head Dashboard:
        '''
        # Total Members of Individual Community (Head Dashboard First Row)
        context["head"] = is_community_head.first()
        
        # Total Deposit of Individual Community (Head Dashboard Second Row)
        context["total_community_members"] = Member.objects.filter(community__community_head=login_user).exclude(role='Community-Head').count() # Exclude Community Head from the total members count
        
        communityHead_total_deposits = individual_deposits.filter(community__community_name=is_community_head.first())
        communityHead_total_deposit = communityHead_total_deposits.aggregate(Sum('total_deposit'))['total_deposit__sum'] or 0
        context["communityHead_total_deposit"] = communityHead_total_deposit
        
        context["communityHead_members_deposit"] = communityHead_total_deposits[:10]

        if is_community_head.exists():
            communityHead_total_loan = loan_dict.get(is_community_head.first().community_name, 0)
            context ['communityHead_total_loan'] = communityHead_total_loan

            highest_borrower = (individual_loans.filter(community__community_name=is_community_head.first()))
            context["community_highest_borrower"] = highest_borrower[:10]

        

        # For Member Dashboard
        if not login_user.is_staff and not is_community_head:
            member_community = login_user.member.community
            context["member_community"] = member_community
            context["member_community_head"] = member_community.community_head.all()

        # Login Member Total Deposit (Member Dashboard)
        context["member_total_deposit"] = individual_deposits.filter(username__first_name=login_user.first_name).first()
        context["member_total_loan"] = individual_loans.filter(username__first_name=login_user.first_name).first()


        context["recent_transactions"] = get_recent_transactions()


        return context

    
    