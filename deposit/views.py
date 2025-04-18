from pyexpat.errors import messages
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy as _
from django.views.generic import TemplateView, CreateView, ListView, View

from django.contrib import messages

from .models import *
from .forms import *


# Create your views here.
class DepositView(ListView):
    model = Deposit
    template_name = "deposit/deposit_list.html"
    context_object_name = "deposits"


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
