from django.contrib import admin

from subscribe.models import SubscribeModel


@admin.register(SubscribeModel)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscriber')
