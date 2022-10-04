from django.contrib import admin

from notifyapp.models import NotifyPostStatus, NotifyLike, NotifyComment, NotifyUserStatus


@admin.register(NotifyPostStatus, NotifyLike, NotifyComment, NotifyUserStatus)
class NotifyAdmin(admin.ModelAdmin):
    pass
