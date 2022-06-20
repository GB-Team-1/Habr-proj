from django.db.models.signals import post_save
from django.dispatch import receiver

from authapp.models import HabrUser
from notifyapp.models import NotifyPostStatus
from posts.models import Posts


@receiver(post_save, sender=Posts)
def notify_post_create(sender, instance, **kwargs):
    moder_users = HabrUser.objects.filter(specialization='Модератор')
    for user in moder_users:
        NotifyPostStatus.objects.create(
            to_user=user,
            to_moder=True,
            notify_body=f'Поступил новый пост на модерацию: {instance.title}',
            post=instance
        )


@receiver(post_save, sender=NotifyPostStatus)
def notify_post_update_status(sender, instance, **kwargs):
    NotifyPostStatus.objects.create()
