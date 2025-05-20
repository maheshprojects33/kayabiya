from django.urls import path
from . import views

urlpatterns = [
    path("deposit-list/", views.DepositView.as_view(), name="deposit_list"),
    path("deposit-create/", views.SingleDepositCreateView.as_view(), name="deposit_create"),
    path("multideposit-create/", views.MultipleDepositCreateView.as_view(), name="multideposit_create"),
    path("deposit-update/<str:pk>/", views.DepositUpdateView.as_view(), name="deposit_update"),
    # path("multideposit-create/", views.MultipleDepositCreateView, name="multideposit_create"),
]

htmx_urlpatterns = [
    path("delete-deposit/<str:pk>/", views.delete_record, name="delete_deposit"),
    # path("create_multiform/", views.delete_record, name="create_multiform"),
]

urlpatterns += htmx_urlpatterns