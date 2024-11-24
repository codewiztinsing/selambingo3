from django.urls import path,include
from .views import UserRegistrationView,FilterUsersByPhoneView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
      path('filter-users/', FilterUsersByPhoneView.as_view(), name='filter_users_by_phone'),
    
]
