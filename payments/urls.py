from django.urls import path
from .views import get_balance,success,error,win,withdraw,loss,get_wallet,commission,withdraw_success,withdraw_error,return_funds,create_payment_session

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
]

