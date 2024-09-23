from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserRegisterView, email_verification, UserProfileView, UserPasswordResetView, EmailNotFoundView

app_name = UsersConfig.name

urlpatterns = [

    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('email_confirm/<str:token>/', email_verification, name='email_confirm'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('email_not_found/', EmailNotFoundView.as_view(), name='email_not_found'),
]
