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
from django.db.models import Q


# Create your views here.
class MemberView(StaffRequiredMixin, ListView):
    model = Member
    template_name = 'member/member_list.html'
    # context_object_name = 'members'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        is_community_head = Community.objects.filter(community_head=user).exists()

        if user.is_staff:
            context["members"] = Member.objects.all()
        elif is_community_head:
            managed_communities = Community.objects.filter(community_head=user)
            context["members"] = Member.objects.filter(
                Q(community__in=managed_communities) | Q(community__isnull=True) 
            ).exclude(role='Community-Head')
            
        return context
    
    # def get_queryset(self):
    #     user = self.request.user

    #     if user.is_staff:
    #         return Member.objects.all()
        
    #     # Get communities this user manages
    #     managed_communities = Community.objects.filter(community_head=user)
    #     return Member.objects.filter(community__in=managed_communities)

        


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
            
            messages.error(self.request, f'Member with name "{new_member }" Already Exists')
            return self.form_invalid(form)
            
        messages.success(self.request, "New Member Account Has Been Created Successfully")
        return super().form_valid(form)


class MemberUpdateView(StaffRequiredMixin, UpdateView):
    model = Member
    form_class = MemberCreationForm
    template_name = 'member/forms/member_update.html'
    success_url = _('member_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["member_name"] = self.object.username.get_full_name()  # or .username if just the username
        return context


    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        user = self.request.user

        if not user.is_staff:
            form.fields["username"].widget = forms.HiddenInput()
            form.fields["community"].widget = forms.HiddenInput()
            form.fields["role"].widget = forms.HiddenInput()
            # Community heads can see but not change the field
            # form.fields["community"].widget.attrs.update({
            #     "class": "form-control",
            #     "readonly": "readonly",
            #     "style": "pointer-events: none; background-color: #e9ecef;" 
            # })
            
        # else:
        #     # Staff can choose the community
        #     form.fields["community"].widget.attrs.update({
        #         "class": "form-control"
        #     })

        return form

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        is_community_head = Community.objects.filter(community_head=user).exists()
        
        if user.is_staff:
            context["communityList"] =  Community.objects.prefetch_related('community_members')
        elif is_community_head:
            context["communityList"] = Community.objects.filter(community_head=user).prefetch_related('community_members')
        
        return context
    
    
class CommunityMemberListView(StaffRequiredMixin, TemplateView):
    template_name = 'community/community_members.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        community = get_object_or_404(Community, pk=self.kwargs['pk'])
        context['community'] = community
        context['members'] = community.community_members.all().exclude(role='Community-Head') # Exclude Community Head from the members list
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
