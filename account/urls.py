from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from . import views


urlpatterns = [
    path("", views.UserLoginView.as_view(), name="login"),

    path("account/", views.AccountView.as_view(), name="account"),
    
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(next_page='/'), name="logout"),

    path("reset-password/<str:pk>/", views.UserPasswordResetView.as_view(), name="reset_password" ),
    path("change-password/", views.UserPasswordChangeView.as_view(), name="change_password" ),

    path('update-user/<str:pk>/', views.UserUpdateView.as_view(), name='update_user'),
    path('delete-user/<str:pk>/', views.UserDeleteView.as_view(), name='delete_user'),
]

