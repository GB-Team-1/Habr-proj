from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from authapp.models import HabrUser
from notifyapp.models import NotifyPostStatus, NotifyComment
from notifyapp.services import send_notification
from posts.models import Posts, Comment


@receiver(post_save, sender=Posts)
def notify_post_create(sender, instance, created, **kwargs):
    if created:
        moder_users = HabrUser.objects.filter(specialization='Модератор')
        for user in moder_users:
            notify = NotifyPostStatus.objects.create(
                to_user=user,
                to_moder=True,
                notify_body=f'Поступил новый пост на модерацию: {instance.title}',
                post=instance
            )
            # send_notification(notify)


@receiver(post_save, sender=Comment)
def notify_post_comment(sender, instance, created, **kwargs):
    if created:
        user = HabrUser.objects.get(username=instance.post.user)
        notify = NotifyComment.objects.create(
            to_user=user,
            notify_body=f'К Хабу {instance.post.title} пользователь {instance.user} оставил комментарий',
            comment=instance
        )
        # send_notification(notify)
