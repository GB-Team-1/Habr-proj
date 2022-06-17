from uuid import uuid4

from django.db import models

from authapp.models import HabrUser
from posts.models import Posts, Comment, Likes


class BaseNotification(models.Model):
    STATUS_CREATE = 'CR'
    STATUS_SEND_PROCESS = 'PR'
    STATUS_SEND_COMPLETED = 'CPT'
    STATUS_ERROR = 'ERR'

    SEND_STATUSES = (
        (STATUS_CREATE, 'Создано'),
        (STATUS_SEND_PROCESS, 'Процесс отправки'),
        (STATUS_SEND_COMPLETED, 'Отправка успешна'),
        (STATUS_ERROR, 'Ошибка отправки'),
    )

    uid = models.UUIDField(primary_key=True, default=uuid4)

    to_user = models.ForeignKey(
        HabrUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователю'
    )
    post = models.ForeignKey(Posts, blank=True, null=True, on_delete=models.CASCADE)
    like = models.ForeignKey(Likes, blank=True, null=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, blank=True, null=True, on_delete=models.CASCADE)
    notify_body = models.TextField(blank=True, verbose_name='Содержание уведомления')
    status_send = models.CharField(max_length=3, choices=SEND_STATUSES,
                                   default=STATUS_CREATE, verbose_name='Статус отпраки')
    status = models.CharField(max_length=3, blank=True, null=True)
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    to_moder = models.BooleanField(default=False, verbose_name='Для модератора')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        abstract = True

    def get_all_notify(self, pk):
        post_query = self.postnotify.filter(is_read=False, to_user__pk=pk).ordered_by('-created_at')
        like_query = self.likenotify.filter(is_read=False, to_user__pk=pk).ordered_by('-created_at')
        comment_query = self.commentnotify.filter(is_read=False, to_user__pk=pk).ordered_by('-created_at')
        user_query = NotifyUserStatus.objects.filter(is_read=False, to_user__pk=pk).ordered_by('-created_at')
        return post_query.union(like_query.union(comment_query.union(user_query)))


class NotifyPostStatus(BaseNotification):
    POST_NEW = 'NEW'
    POST_TO_MODERATION = 'TO'
    POST_MODERATED = 'MOD'
    POST_BLOCKED = 'BLC'
    POST_DELETED = 'DEL'
    POST_STATUSES = (
        (POST_NEW, 'Поступил новый на модерацию'),
        (POST_TO_MODERATION, 'На модерации'),
        (POST_MODERATED, 'Прошел модерацию'),
        (POST_BLOCKED, 'Заблокирован (не прошел модерацию)'),
        (POST_DELETED, 'Удален'),
    )
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='postnotify', verbose_name='Хаб')
    status = models.CharField(max_length=3, choices=POST_STATUSES,
                              default=POST_TO_MODERATION, verbose_name='Статус хаба')

    class Meta:
        verbose_name = 'Уведомление по хабу'
        verbose_name_plural = 'Уведомления по хабам'


class NotifyLike(BaseNotification):
    like = models.ForeignKey(Likes, on_delete=models.CASCADE, related_name='likenotify', verbose_name='Лайк')

    class Meta:
        verbose_name = 'Уведомление по лайкам'
        verbose_name_plural = 'Уведомления по лайкам'


class NotifyComment(BaseNotification):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,
                                related_name='commentnotify', verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Уведомление по комментариям'
        verbose_name_plural = 'Уведомления по комментариям'


class NotifyUserStatus(BaseNotification):
    USER_REGISTER = 'REG'
    USER_ACTIVE = 'ACT'
    USER_BLOCKED = 'BLC'
    USER_DELETE = 'DEL'
    USER_STATUSES = (
        (USER_REGISTER, 'Пользователь зарегистрирован'),
        (USER_ACTIVE, 'Учетная  запись активирована'),
        (USER_BLOCKED, 'Учетная запись временно заблокирована'),
        (USER_DELETE, 'Учетная запись удалена'),
    )
    status = models.CharField(max_length=3, choices=USER_STATUSES,
                              default=USER_REGISTER, verbose_name='Статус пользователя')

    class Meta:
        verbose_name = 'Уведомление по пользователю'
        verbose_name_plural = 'Уведомления по пользователю'
