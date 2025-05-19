from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from member.models import Community


class StaffRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        is_community_head = Community.objects.filter(community_head=user).exists()
        # Check if the user is logged in and is a staff member
        if not request.user.is_staff and not is_community_head:
            return redirect("/")  # Redirect to homepage
        return super().dispatch(request, *args, **kwargs)
    # pass
