from django.urls import path,include
from .views import check_balance_view,WalletBalanceView

urlpatterns = [
    path('balance/', check_balance_view),
    path('wallets/balance/', WalletBalanceView.as_view(), name='wallet-balance'),
    path("payments/",include("payments.urls"))

]
