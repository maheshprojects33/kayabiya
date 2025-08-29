from django.urls import path
from . import views

urlpatterns = [
    # path('loan-list/', views.LoanListView.as_view(), name='loan_list'),
    path('loan-request/', views.LoanRequestView.as_view(), name='loan_request'),
    path('loan-disbursed/', views.LoanDisbursedView.as_view(), name='loan_disbursed'),
    path('loan-settled/', views.LoanSettledView.as_view(), name='loan_settled'),
    path('loan-voided/', views.LoanVoidedView.as_view(), name='loan_voided'),
    path('loan-watchlist/', views.LoanWatchlistView.as_view(), name='loan_watchlist'),

    path('loan-apply/', views.LoanApplyView.as_view(), name='loan_apply'),
    path('loan-update/<str:pk>/', views.LoanUpdateView.as_view(), name='loan_update'),
    
    path('loan-account-create/', views.LoanAccountCreateView.as_view(), name='loan_account_create'),
    path('loan-account-list/', views.LoanAccountListView.as_view(), name='loan_account_list'),

    path('loan-interest-list/<str:pk>/', views.LoanInterestListView.as_view(), name='loan_interest_list'),
    path('loan-interest-update/<str:pk>/', views.LoanInterestUpdateView.as_view(), name='loan_interest_update')


    # path('loan-repay/', views.LoanRepaymentView.as_view(), name='loan_repay'),
   
]
