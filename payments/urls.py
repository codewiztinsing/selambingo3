from django.urls import path
from .views import get_balance,success,error,win,withdraw,loss

urlpatterns = [
    # path('deposit/', pay_with_chapa,name="pay-with-chapa"),
    path('balance/', get_balance,name="get-balance"),
    path('success/', success,name="success"),
    path('win/', win,name="win"),
    path('loss/', loss,name="loss"),
    path('error/', error,name="error"),
    path('withdraw/', withdraw,name="withdraw"),

]

