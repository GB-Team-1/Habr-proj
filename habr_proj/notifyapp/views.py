from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, ListView, DeleteView

from notifyapp.models import NotifyUserStatus, NotifyPostStatus, NotifyLike, NotifyComment, BaseNotification


def get_all_unread_notify(pk):
    post_query = NotifyPostStatus.objects.filter(is_read=False, to_user__pk=pk)
    like_query = NotifyLike.objects.filter(is_read=False, to_user__pk=pk)
    comment_query = NotifyComment.objects.filter(is_read=False, to_user__pk=pk)
    user_query = NotifyUserStatus.objects.filter(is_read=False, to_user__pk=pk)
    return post_query.union(like_query.union(comment_query.union(user_query)))


def get_all_notify(pk):
    post_query = NotifyPostStatus.objects.filter(to_user__pk=pk)
    like_query = NotifyLike.objects.filter(to_user__pk=pk)
    comment_query = NotifyComment.objects.filter(to_user__pk=pk)
    user_query = NotifyUserStatus.objects.filter(to_user__pk=pk)
    return post_query.union(like_query.union(comment_query.union(user_query)))


class NotifyConfirmAllView(DetailView):

    def get_queryset(self):
        return get_all_unread_notify(self.request.user.pk)

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
        context_data['notify'] = get_all_unread_notify(pk=self.request.user.pk)[:5]
        return context_data



class NotifyDetailView(DetailView):
    pass


class NotifyDeleteView(DeleteView):
    pass
