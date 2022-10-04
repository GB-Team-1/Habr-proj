from django.db import models

# Create your models here.
from authapp.models import HabrUser


class SubscribeModel(models.Model):
    user = models.ForeignKey(HabrUser, on_delete=models.CASCADE,
                             related_name='author', verbose_name='Пользователь', default=None)
    subscriber = models.ForeignKey(HabrUser, on_delete=models.CASCADE,
                                   related_name='subscriber', verbose_name='Подписчик', default=None)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
