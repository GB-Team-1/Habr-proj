from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import CreateView

from authapp.forms import HabrUserLoginForm


class LoginUserView(LoginView):
    template_name = 'authapp/login.html'
    form_class = HabrUserLoginForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Вход'

        return context_data


class LogoutUserView(LogoutView):
    template_name = 'authapp/logout.html'

