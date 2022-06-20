from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView

from notifyapp.models import NotifyUserStatus, NotifyPostStatus, NotifyLike, NotifyComment


def get_all_notify(pk):
    post_query = NotifyPostStatus.objects.filter(is_read=False, to_user__pk=pk)
    like_query = NotifyLike.objects.filter(is_read=False, to_user__pk=pk)
    comment_query = NotifyComment.objects.filter(is_read=False, to_user__pk=pk)
    user_query = NotifyUserStatus.objects.filter(is_read=False, to_user__pk=pk)
    return post_query.union(like_query.union(comment_query.union(user_query)))


class NotifyConfirmAllView(DetailView):

    def get_queryset(self):
        return get_all_notify(self.request.user.pk)

    def get(self, request, *args, **kwargs):
        notifications = self.get_queryset()
        for notify in notifications:
            notify.is_read = True
            notify.save()
        return HttpResponseRedirect(reverse('main'))
