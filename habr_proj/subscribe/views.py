from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import RedirectView, TemplateView

from authapp.models import HabrUser
from subscribe.models import SubscribeModel


class SubscribeView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        user_pk = self.kwargs.get('pk')
        return reverse_lazy('auth:user_profile', kwargs={'pk': user_pk})

    def get(self, request, *args, **kwargs):
        user = HabrUser.objects.filter(pk=self.kwargs.get('pk')).first()
        SubscribeModel.objects.create(user=user, subscriber=self.request.user)
        return super(SubscribeView, self).get(request, *args, **kwargs)


class UnSubscribeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user_pk = self.kwargs.get('pk')
        return reverse_lazy('auth:user_profile', kwargs={'pk': user_pk})

    def get(self, request, *args, **kwargs):
        user = HabrUser.objects.filter(pk=self.kwargs.get('pk')).first()
        SubscribeModel.objects.get(user=user, subscriber=self.request.user).delete()
        return super(UnSubscribeView, self).get(request, *args, **kwargs)


class FollowersView(TemplateView):
    template_name = 'subscribe/followers.html'

    def get_context_data(self, **kwargs):
        user = HabrUser.objects.get(pk=self.kwargs.get('pk'))
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Подписчики {user.username}'
        context_data['followers'] = SubscribeModel.objects.filter(user=user)
        context_data['user_followings'] = SubscribeModel.objects.filter(subscriber=self.request.user).values_list('user__username')
        context_data['username'] = user.username
        context_data['pk'] = self.kwargs.get('pk')
        return context_data


class SubscribesView(TemplateView):
    template_name = 'subscribe/subscriptions.html'

    def get_context_data(self, **kwargs):
        user = HabrUser.objects.get(pk=self.kwargs.get('pk'))
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Подписки {user.username}'
        context_data['subscribes'] = SubscribeModel.objects.filter(subscriber=user)
        context_data['user_followings'] = SubscribeModel.objects.filter(subscriber=self.request.user).values_list('user__username')
        context_data['username'] = user.username
        return context_data