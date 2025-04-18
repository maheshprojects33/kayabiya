from datetime import datetime
from multiprocessing import context
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy as _
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from account.mixins import StaffRequiredMixin


from .models import *
from .forms import *

from django.contrib.auth.models import User


# Create your views here.
class MemberView(StaffRequiredMixin, ListView):
    model = Member
    template_name = 'member/member_list.html'
    context_object_name = 'members'

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Member.objects.all()
        
        # Get communities this user manages
        managed_communities = Community.objects.filter(community_head=user)
        return Member.objects.filter(community__in=managed_communities)

        


class MemberCreateView(CreateView):
    model = Member
    form_class = MemberCreationForm
    template_name = 'member/forms/member_create.html'
    success_url = _("member_list")

    def form_valid(self, form):
        # Get Name from Filled Form
        new_member = form.cleaned_data['username']

        # Check if a member with the same name already exists
        if Member.objects.filter(username=new_member).exists():
            print("Member Already Exist")
            messages.error(self.request, f'Member with name "{new_member }" Already Exists')
            return self.form_invalid(form)
            # else:
            #     user = form.save()
            #     User.objects.create(
            #         username=user.username,
            #     )
            messages.success(self.request, "New Member Account Has Been Created Successfully")
        return super().form_valid(form)


class MemberUpdateView(StaffRequiredMixin, UpdateView):
    model = Member
    form_class = MemberCreationForm
    template_name = 'member/forms/member_update.html'
    success_url = _('member_list')

    def form_valid(self, form):
        dob = form.cleaned_data['dob']
        current_date = datetime.now().date()

        # Checking entry for Date of Birth
        if dob:
            if dob >= current_date:
                messages.warning(self.request, "Birth Date Must Be Earlier Than Today's Date")
                return self.form_invalid(form)
        else:
            pass

        return super().form_valid(form)


class MemberDeleteView(StaffRequiredMixin, DeleteView):
    model = Member
    template_name = 'member/forms/member_delete.html'
    success_url = _('member_list')

class CommunityListView(StaffRequiredMixin, ListView):
    model = Community
    template_name = 'community/community_list.html'
    context_object_name = 'communityList'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Community.objects.prefetch_related('community_members')
        elif Community.objects.filter(community_head=user).exists():
            return Community.objects.filter(community_head=user).prefetch_related('community_members')
        else:
            return Community.objects.none()
    
class CommunityMemberListView(StaffRequiredMixin, TemplateView):
    template_name = 'community/community_members.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        community = get_object_or_404(Community, pk=self.kwargs['pk'])
        context['community'] = community
        context['members'] = community.community_members.all()
        return context

class CommunityCreateView(CreateView):
    model = Community
    form_class = CommunityCreationForm
    template_name = 'community/forms/community_create.html'
    success_url = _("community_list")

class CommunityUpdateView(StaffRequiredMixin, UpdateView):
    model = Community
    form_class = CommunityCreationForm
    template_name = 'community/forms/community_update.html'
    success_url = _('community_list')

class CommunityDeleteView(StaffRequiredMixin, DeleteView):
    model = Community
    template_name = 'community/forms/community_delete.html'
    success_url = _('community_list')
