from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models


class HabrUser(AbstractUser):
    uid = models.UUIDField(primary_key=True, default=uuid4)
    avatar = models.ImageField(upload_to='user_avatar', blank=True, verbose_name='Аватар')
    birthday = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    about_me = models.TextField(max_length=512, blank=True, verbose_name='Обо мне')
    specialization = models.CharField(max_length=150, blank=True, null=True, verbose_name='Специализация')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def activate_user(self):
        self.is_active = True
        self.save()
