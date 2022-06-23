from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from authapp.models import HabrUser
from notifyapp.models import NotifyPostStatus, NotifyComment, NotifyLike
from notifyapp.services import send_notification
from posts.models import Posts, Comment, PostsLikes


@receiver(post_save, sender=Posts)
def notify_post_create(sender, instance, created, **kwargs):
    if created:
        moder_users = HabrUser.objects.filter(is_staff=True)
        category = 'PST'
        for user in moder_users:
            notify = NotifyPostStatus.objects.create(
                to_user=user,
                category=category,
                to_moder=True,
                notify_body=f'Поступил новый пост на модерацию: {instance.title}',
                post=instance
            )
            # send_notification(notify)


@receiver(pre_save, sender=Posts)
def notify_post_moderated(sender, instance, **kwargs):
    old_post = Posts.objects.get(pk=instance.pk)
    if old_post:
        old_moder_status = old_post.is_moderated
        new_moder_status = instance.is_moderated
        if old_moder_status != new_moder_status:
            notify_set = NotifyPostStatus.objects.filter(post=instance)
            for notify in notify_set:
                if instance.is_moderated:
                    notify.status = 'MOD'
                    notify.to_user = instance.user
                    notify.is_read = False
                    notify.notify_body = f'Пост {instance.title} прошел модерацию'
                    notify.save()
                else:
                    notify.status = 'BLC'
                    notify.to_user = instance.user
                    notify.is_read = False
                    notify.notify_body = f'Пост {instance.title} не прошел модерацию!'
                    notify.save()
            # send_notification(notify)


@receiver(post_save, sender=Comment)
def notify_post_comment(sender, instance, created, **kwargs):
    if created:
        user = HabrUser.objects.get(username=instance.post.user)
        category = 'CMT'
        notify = NotifyComment.objects.create(
            to_user=user,
            category=category,
            notify_body=f'К Хабу {instance.post.title} пользователь {instance.user} оставил комментарий',
            comment=instance
        )
        # send_notification(notify)


@receiver(post_save, sender=PostsLikes)
def notify_like_post(sender, instance, created, **kwargs):
    if created:
        user = instance.post.user
        category = 'LK'
        notify = NotifyLike.objects.create(
            to_user=user,
            category=category,
            notify_body=f'К Хабу {instance.post.title} пользователь {instance.user} поставил лайк',
            like=instance
        )
        # send_notification(notify)


@receiver(post_save, sender=Comment)
def notify_comment_to_moder(sender, instance, created, **kwargs):
    if created and '@moderator' in instance.comment_body:
        moder_users = HabrUser.objects.filter(is_staff=True)
        category = 'CMT'
        for user in moder_users:
            notify = NotifyComment.objects.create(
                to_user=user,
                to_moder=True,
                category=category,
                notify_body=f'К Хабу {instance.post.title} пользователь {instance.user} оставил комментарий'
                            f' c обращением к модератору.',
                comment=instance
            )
