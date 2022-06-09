from django.contrib import auth
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView, DetailView
from authapp.forms import HabrUserLoginForm, HabrUserRegisterForm, HabrUserEditForm
from authapp.models import HabrUser
from authapp.services import send_verify_email
from posts.models import PostCategory, Posts


class LoginUserView(LoginView):
    template_name = 'authapp/auth-login.html'
    form_class = HabrUserLoginForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Вход'
        context_data['categories'] = PostCategory.objects.filter()
        return context_data


class LogoutUserView(LogoutView):
    template_name = 'authapp/logout.html'


class RegisterUserView(CreateView):
    form_class = HabrUserRegisterForm
    template_name = 'authapp/auth-register.html'
    success_url = reverse_lazy("auth:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['categories'] = PostCategory.objects.filter()
        return context

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


class UpdateProfileView(UpdateView):
    form_class = HabrUserEditForm
    template_name = 'authapp/profile.html'
    success_url = reverse_lazy('authapp:profile')

    def get_object(self, queryset=None):
        if self.request.user.is_anonymous:
            return None
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование профиля'
        context['categories'] = PostCategory.objects.filter()
        context['posts_count'] = Posts.objects.filter(user=self.request.user, is_published=True,is_active=True).count()
        return context

    def get(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse('auth:login'))
        return super(UpdateProfileView, self).get(request, *args, **kwargs)


class UserProfileDetailView(DetailView):
    template_name = 'authapp/profile_detail.html'

    def get_queryset(self):
        return HabrUser.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль'
        context['user_detail'] = self.get_queryset().first()
        context['count_posts'] = Posts.objects.filter(user__pk=self.kwargs.get('pk'), is_published=True, is_active=True).count()
        context['posts'] = Posts.objects.filter(user__pk=self.kwargs.get('pk'), is_published=True, is_active=True).order_by('-created_at')
        return context
