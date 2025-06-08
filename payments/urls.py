from django.urls import path
from .views import *

urlpatterns = [
    # path('deposit/', pay_with_chapa,name="pay-with-chapa"),
    path('balance/', get_balance,name="get-balance"),
    path('returnFunds/', return_funds,name="return-funds"),
    path('success/', success,name="success"),
    path('win/', win,name="win"),
    path('loss/', loss,name="loss"),
    path('error/', error,name="error"),
    path('withdraw/', withdraw,name="withdraw"),
    path('withdraw/success/', success,name="withdraw-success"),
    path('withdraw/error/', error,name="withdraw-error"),
    path('wallet/<str:user_id>/', get_wallet,name="get-wallet"),
    path('commission/', commission,name="commission"),
    path('session/', create_payment_session,name="create-payment-session"),
    path("notifyUrl/", notify_url,name="notify-url"),
    path("notifyUrl-withdraw/", notify_url_withdraw,name="notify-url-withdraw"),
    path('deposit/', deposit,name="deposit"),
    path('message/', deposit_message,name="deposit-message"),
]

