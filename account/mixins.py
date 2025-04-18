from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin


class StaffRequiredMixin(LoginRequiredMixin):
    # def dispatch(self, request, *args, **kwargs):
    #     # Check if the user is logged in and is a staff member
    #     if not request.user.is_staff:
    #         return redirect("/")  # Redirect to homepage
    #     return super().dispatch(request, *args, **kwargs)
    pass
