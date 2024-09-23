import random
import secrets
import string

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm, UserPasswordResetForm
from users.models import User


class UserRegisterView(CreateView):
    """Класс-контроллер для регистрации нового пользователя"""
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Метод, отправляющий письмо с токеном для подтверждения почты при регистрации"""
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)  # генерируем token для отправки пользователю (import secrets)
        user.token = token
        user.save()  # сохраняем пользователя в БД
        host = self.request.get_host()  # получаем хост, откуда пришел пользователь
        url = f'http://{host}/users/email_confirm/{token}'  # генерируем пользователю ссылку для перехода
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет! Перейди по ссылке для подтверждения почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    """Подтверждение регистрации переход по ссылке из письма и редирект на страницу входа"""
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()  # сохраняем пользователя в БД
    return redirect(reverse('users:login'))


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordResetView(PasswordResetView):
    """Сброс пароля"""
    template_name = 'users/user_password_reset.html'
    form_class = UserPasswordResetForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            if user:
                password = User.objects.make_random_password(length=10)
                user.set_password(password)
                user.save()
                send_mail(
                    subject='Сброс пароля',
                    message=f' Ваш новый пароль {password}',
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email]
                )
            return redirect(reverse('users:login'))
        except:
            return redirect(reverse('users:email_not_found'))


class EmailNotFoundView(TemplateView):
    """Отправка ответа об отсутствии почты"""
    template_name = 'users/email_not_found.html'