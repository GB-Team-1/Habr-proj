from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from authapp.models import HabrUser
from notifyapp.models import NotifyPostStatus, NotifyComment
from posts.models import Posts, Comment


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


# @receiver(pre_save, sender=NotifyPostStatus)
# def notify_post_update_status(sender, instance, **kwargs):
#     user = HabrUser.objects.get(username=instance.post.user)
#     instance.to_user = user
#     instance.notify_body = f'Изменилось состояние хаба {instance.post.title}: {instance.status}'
#     instance.save()

@receiver(post_save, sender=Comment)
def notify_post_comment(sender, instance, created, **kwargs):
    if created:
        user = HabrUser.objects.get(username=instance.post.user)
        NotifyComment.objects.create(
            to_user=user,
            notify_body=f'К Хабу {instance.post.title} пользователь {instance.user} оставил комментарий',
            comment=instance
        )
