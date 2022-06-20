from django.shortcuts import render

from notifyapp.models import NotifyUserStatus, NotifyPostStatus, NotifyLike, NotifyComment


def get_all_notify(pk):
    post_query = NotifyPostStatus.objects.filter(is_read=False, to_user__pk=pk)
    like_query = NotifyLike.objects.filter(is_read=False, to_user__pk=pk)
    comment_query = NotifyComment.objects.filter(is_read=False, to_user__pk=pk)
    user_query = NotifyUserStatus.objects.filter(is_read=False, to_user__pk=pk)
    return post_query.union(like_query.union(comment_query.union(user_query)))
