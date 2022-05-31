from django.contrib import auth
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView
from authapp.forms import HabrUserLoginForm, HabrUserRegisterForm
from authapp.models import HabrUser
from authapp.services import send_verify_email


class LoginUserView(LoginView):
    template_name = 'authapp/login.html'
    form_class = HabrUserLoginForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Вход'

        return context_data


class LogoutUserView(LogoutView):
    template_name = 'authapp/logout.html'


class RegisterUserView(CreateView):
    form_class = HabrUserRegisterForm
    template_name = 'authapp/register.html'
    success_url = reverse_lazy("auth:login")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            new_user = form.save()
            send_verify_email(new_user)
            return HttpResponseRedirect(reverse('auth:login'))
        return super(RegisterUserView, self).post(request, *args, **kwargs)


class VerifyUserView(View):
    def get(self, request, key):
        user = HabrUser.objects.filter(uid=key).first()
        if user:
            user.activate_user()
            auth.login(request, user)
        return render(request, 'authapp/register_result.html')
