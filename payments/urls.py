from django.urls import path
from .views import get_balance,success,error,win,withdraw,loss,get_wallet,commission,withdraw_success,withdraw_error

urlpatterns = [
    # path('deposit/', pay_with_chapa,name="pay-with-chapa"),
    path('balance/', get_balance,name="get-balance"),
    path('success/', success,name="success"),
    path('win/', win,name="win"),
    path('loss/', loss,name="loss"),
    path('error/', error,name="error"),
    path('withdraw/', withdraw,name="withdraw"),
    path('withdraw/success/', success,name="withdraw-success"),
    path('withdraw/error/', error,name="withdraw-error"),
    path('wallet/<str:username>/', get_wallet,name="get-wallet"),
    path('commission/', commission,name="commission"),

]

