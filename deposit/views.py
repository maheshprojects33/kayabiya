from multiprocessing import context
from pyexpat.errors import messages
from django.forms import BaseModelForm, modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy as _
from django.views.generic import TemplateView, CreateView, ListView, View, UpdateView

from django.contrib import messages

from member.admin import CommunityAdmin

from .models import *
from .forms import *

from member.models import Community
from account.mixins import StaffRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class DepositView(LoginRequiredMixin, ListView):
    model = Deposit
    template_name = "deposit/deposit_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        login_user = self.request.user

        is_community_head = Community.objects.filter(community_head=login_user)
        context["is_community_head"] = is_community_head.exists()

        if login_user.is_staff:
            context["deposits"] = Deposit.objects.all()
        elif is_community_head.exists():
            # Community head sees deposits of members in their managed communities
            
            members = Member.objects.filter(community__in=is_community_head)
            context["deposits"] = Deposit.objects.filter(account__in=members)
        else:
             # Normal member sees only their own deposits
            
            member = Member.objects.get(username=login_user)
            context["deposits"] = Deposit.objects.filter(account=member)
            
        

        return context


class SingleDepositCreateView(StaffRequiredMixin, CreateView):
    model = Deposit
    form_class = DepositForm
    template_name = "deposit/forms/single_deposit_create.html"
    success_url = _("deposit_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        current_date = datetime.now().date()
        

        if form.cleaned_data["date"] > current_date:
            messages.warning(self.request, "Future Date Is Not Acceptable")
            return self.form_invalid(form)
        messages.success(self.request, "New Deposit Has Been Added Successfully")
        return super().form_valid(form)


class MultipleDepositCreateView(View):
    template_name = 'deposit/forms/multiple_deposit_create.html'
    success_url = _("deposit_list")

    def get(self, request, *args, **kwargs):
        DepositFormSet = modelformset_factory(Deposit, form=DepositForm, extra=5)
        formset = DepositFormSet(queryset=Deposit.objects.none(), form_kwargs={'user': request.user})
        return render(request, self.template_name, {'formset': formset})

    def post(self, request, *args, **kwargs):
        DepositFormSet = modelformset_factory(Deposit, form=DepositForm, extra=5)
        formset = DepositFormSet(request.POST, form_kwargs={'user': request.user})
        if formset.is_valid():
            formset.save()
            messages.success(request, "Deposits added successfully!")
            return redirect(self.success_url)
        return render(request, self.template_name, {'formset': formset})


class DepositUpdateView(StaffRequiredMixin, UpdateView):
    model = Deposit
    form_class = DepositForm
    template_name = "deposit/forms/deposit_update.html"
    success_url = _("deposit_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs



# All Codes for htmx
from django.shortcuts import get_object_or_404, redirect


def delete_record(request, pk):
    deposit = get_object_or_404(Deposit, pk=pk)
    deposit.delete()

    deposits = Deposit.objects.all()

    return render(request, "deposit/htmx_deposit_list.html", {"deposits": deposits})
