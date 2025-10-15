from django.urls import path
from .views import * 

urlpatterns = [
    path('login', user_login, name='user_login'),
    path('logout', user_logout, name='user_logout'),
    path('password-reset', password_reset, name='password_reset'),
    path('confirm-reset-password', confirm_password_reset, name='reset_password'),
]
