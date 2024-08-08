from django.urls import path
from .views import check_balance_view

urlpatterns = [
    path('balance/', check_balance_view),
]
