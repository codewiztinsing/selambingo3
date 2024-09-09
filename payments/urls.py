from django.urls import path
from .views import pay_with_chapa

urlpatterns = [
    path('deposit/', pay_with_chapa,name="pay-with-chapa"),
  

]
