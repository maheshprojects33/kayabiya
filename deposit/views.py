from multiprocessing import context
from pyexpat.errors import messages
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy as _
from django.views.generic import TemplateView, CreateView, ListView, View

from django.contrib import messages

from member.admin import CommunityAdmin

from .models import *
from .forms import *

from member.models import Community


# Create your views here.
class DepositView(ListView):
    model = Deposit
    template_name = "deposit/deposit_list.html"
    # context_object_name = "deposits"

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
            print(members)
            context["deposits"] = Deposit.objects.filter(account__in=members)
        else:
             # Normal member sees only their own deposits
            
            member = Member.objects.get(username=login_user)
            context["deposits"] = Deposit.objects.filter(account=member)
            
        

        return context


class SingleDepositCreateView(CreateView):
    model = Deposit
    form_class = DepositForm
    template_name = "deposit/forms/single_deposit_create.html"
    success_url = _("deposit_list")

    def form_valid(self, form):
        current_date = datetime.now().date()
        

        if form.cleaned_data["date"] > current_date:
            messages.warning(self.request, "Future Date Is Not Acceptable")
            return self.form_invalid(form)
        messages.success(self.request, "New Deposit Has Been Added Successfully")
        return super().form_valid(form)


# class MultipleDepositCreateView(CreateView):
#     model = Deposit
#     form_class = SingleDepositForm
#     template_name = 'deposit/forms/multiple_deposit_create.html'


def MultipleDepositCreateView(request):
    context = {"form": DepositForm()}
    return render(request, "deposit/forms/multiple_deposit_create.html", context)


# All Codes for htmx
from django.shortcuts import get_object_or_404, redirect


def delete_record(request, pk):
    deposit = get_object_or_404(Deposit, pk=pk)
    deposit.delete()

    deposits = Deposit.objects.all()

    return render(request, "deposit/htmx_deposit_list.html", {"deposits": deposits})
