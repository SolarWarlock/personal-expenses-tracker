# expenses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('expense/add/', views.ExpenseCreateView.as_view(), name='expense_add'),
    path('transfer/add/', views.TransferCreateView.as_view(), name='transfer_add'),
    path('history/', views.HistoryView.as_view(), name='history'),
]