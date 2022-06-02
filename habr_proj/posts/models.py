from django.db import models


class PostCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'