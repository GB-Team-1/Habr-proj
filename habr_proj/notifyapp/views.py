from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, ListView, DeleteView

from notifyapp.models import NotifyUserStatus, NotifyPostStatus, NotifyLike, NotifyComment, BaseNotification
from posts.views import get_categories


def get_all_unread_notify(pk):
    post_query = NotifyPostStatus.objects.filter(is_read=False, to_user__pk=pk)
    like_query = NotifyLike.objects.filter(is_read=False, to_user__pk=pk)
    comment_query = NotifyComment.objects.filter(is_read=False, to_user__pk=pk)
    user_query = NotifyUserStatus.objects.filter(is_read=False, to_user__pk=pk)
    return post_query.union(like_query, comment_query, user_query).order_by('-created_at').count()


def get_all_notify(pk):
    post_query = NotifyPostStatus.objects.filter(to_user__pk=pk)
    like_query = NotifyLike.objects.filter(to_user__pk=pk)
    comment_query = NotifyComment.objects.filter(to_user__pk=pk)
    user_query = NotifyUserStatus.objects.filter(to_user__pk=pk)
    return post_query.union(like_query, comment_query, user_query).order_by('-created_at')


def get_notify(pk, category):
    categories = {
        'PST': NotifyPostStatus,
        'LK': NotifyLike,
        'CMT': NotifyComment,
        'USR': NotifyUserStatus
    }

    return categories[category].objects.filter(pk=pk)


class NotifyConfirmAllView(DetailView):

    def get_queryset(self):
        return get_all_notify(self.request.user.pk)

    def get(self, request, *args, **kwargs):
        notifications = self.get_queryset()
        for notify in notifications:
            notify.is_read = True
            notify.save()
        return HttpResponseRedirect(reverse('main'))


class NotifyListView(ListView):
    template_name = 'notifyapp/notify_list.html'

    def get_queryset(self):
        return get_all_notify(self.request.user.pk)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = f'Уведомления {self.request.user}'
        context_data['notify_list'] = self.get_queryset()
        context_data['categories'] = get_categories()
        context_data['notify'] = get_all_notify(pk=self.request.user.pk)[:5]
        context_data['notify_count'] = get_all_unread_notify(pk=self.request.user.pk)
        return context_data


class NotifyReadView(DetailView):

    def get_queryset(self):
        return get_notify(self.kwargs.get('pk'), self.kwargs.get('category'))

    def get(self, request, *args, **kwargs):
        notify = self.get_queryset().first()
        if not notify.is_read:
            notify.is_read = True
        else:
            notify.is_read = False
        notify.save()
        return HttpResponseRedirect(reverse('notify:notify_list'))


class NotifyDeleteView(DeleteView):

    def get_queryset(self):
        return get_notify(self.kwargs.get('pk'), self.kwargs.get('category'))

    def get(self, request, *args, **kwargs):
        notify = self.get_queryset().first()
        notify.delete()
        return HttpResponseRedirect(reverse('notify:notify_list'))
