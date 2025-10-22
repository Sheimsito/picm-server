from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import * 

urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='user_login'),
    path('refresh-token', TokenRefreshView.as_view(), name='refresh_token'),
    path('logout', user_logout, name='user_logout'),
    path('password-reset', password_reset, name='password_reset'),
    path('confirm-reset-password', confirm_password_reset, name='reset_password'),
    path('get-users-name', get_users_name, name='get_users_name'),
]
