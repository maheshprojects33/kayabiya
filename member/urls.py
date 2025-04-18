from django.urls import path
from . import views

urlpatterns = [
    path("member-list/", views.MemberView.as_view(), name="member_list"),
    path("create-member/", views.MemberCreateView.as_view(), name="create_member"),
    path("update-member/<str:pk>/", views.MemberUpdateView.as_view(), name="update_member"),
    path("delete-member/<str:pk>/", views.MemberDeleteView.as_view(), name="delete_member"),
    
    path("community-list/", views.CommunityListView.as_view(), name="community_list"),
    # path("community-list/<str:pk>/", views.CommunityListView.as_view(), name="community_member"),
    path("community-list/<str:pk>/", views.CommunityMemberListView.as_view(), name="community_member"),
    path("update-community/<str:pk>/", views.CommunityUpdateView.as_view(), name="update_community"),
    path("delete-community/<str:pk>/", views.CommunityDeleteView.as_view(), name="delete_community"),

    path("create-community/", views.CommunityCreateView.as_view(), name="create_community"),
]
