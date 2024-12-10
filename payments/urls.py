from django.urls import path
from .views import get_balance

urlpatterns = [
    # path('deposit/', pay_with_chapa,name="pay-with-chapa"),
    path('balance/', get_balance,name="get-balance"),
]
