from django.urls import path
from . import views

app_name = 'support'
urlpatterns = [
    path('login/', views.support_login, name='support_login'),

    path('dashboard/', views.support_dashboard, name='support_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('payment-requests/', views.payment_requests, name='payment_requests'),
    path('approve-withdrawal/<int:id>/', views.approve_withdrawal, name='approve_withdrawal'),
    path('reject-withdrawal/<int:id>/', views.reject_withdrawal, name='reject_withdrawal'),
    path('transcations/', views.transcations, name='transcations'),
    path('reports/', views.reports, name='reports'),
    path('users/', views.users, name='users'),
    path('settings/', views.settings, name='settings'),
]
