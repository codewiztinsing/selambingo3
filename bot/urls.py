from django.urls import path,include
from .views import check_balance_view,WalletBalanceView

urlpatterns = [
    path("payments/",include("payments.urls")),
    path("accounts/",include("accounts.urls"))
]
