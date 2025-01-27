from django.urls import path,include
from .views import UserRegistrationView,FilterUsersByPhoneView,AllUsersView,login,logout


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', login, name='login'),
    path('filter-users/<int:user_id>/', FilterUsersByPhoneView.as_view(), name='filter_users_by_phone'),
    path('all-users/', AllUsersView.as_view(), name='all_users'),
    path('logout/', logout, name='logout'),

]
