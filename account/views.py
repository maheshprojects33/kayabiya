from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, View
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy as _
from django.views.generic import CreateView
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import *
from .mixins import StaffRequiredMixin

from member.models import Member, Community


# Create your views here.
class AccountView(StaffRequiredMixin, ListView):
    model = User
    template_name = "account/account_list.html"
    context_object_name = "users"

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return User.objects.all()
        
        # Get communities this user manages
        managed_communities = Community.objects.filter(community_head=user)

        # Return all members in those communities
        member_users = Member.objects.filter(community__in=managed_communities).values_list('username', flat=True)

        return User.objects.filter(id__in=member_users)



class UserRegisterView(StaffRequiredMixin, CreateView):
    template_name = "account/forms/account_create.html"
    form_class = UserRegistrationForm
    success_url = _("account")  # Redirect to login page after successful registration

    def form_valid(self, form):
        user = form.save()

        # To Create New Member Automatically
        Member.objects.create(username=user)

        messages.success(self.request, "User Account Has Been Created Successfully")
        return super().form_valid(form)


# Reset Passwords From Admin Panel to Reset User's Password
class UserPasswordResetView(StaffRequiredMixin, FormView):
    form_class = UserPasswordResetForm
    template_name = "account/forms/password_reset.html"

    def get_form(self, form_class=None):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        return self.form_class(user=user, **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()

        messages.success(self.request, "Password changed successfully.")
        return redirect("account")


# Reset Password For Users to Reset their own Password
class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = "account/forms/user_password_change.html"
    success_url = _("dashboard")


from django.contrib.auth import get_user


class UserUpdateView(StaffRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "account/forms/update_user.html"
    success_url = _("account")

    def form_valid(self, form):
        messages.success(self.request, "User details updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Error updating user details. Please correct the form and try again.",
        )
        return super().form_invalid(form)


class UserDeleteView(StaffRequiredMixin, DeleteView):
    model = User
    template_name = "account/forms/delete_user.html"
    success_url = _("account")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "User has been deleted successfully.")
        return super().delete(request, *args, **kwargs)


class UserLoginView(LoginView):
    template_name = "account/forms/account_login.html"
    redirect_authenticated_user = True
    next_page = _("dashboard")

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)
