from uuid import uuid4

from django.db import models

from authapp.models import HabrUser


class PostCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_posts(self):
        return self.posts.select_related()

    def __str__(self):
        return f'{self.name}'


class Posts(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid4)
    user = models.ForeignKey(HabrUser, on_delete=models.CASCADE,
                             related_name='userpost', verbose_name='Пользователь', default=None)
    category = models.ForeignKey(PostCategory, on_delete=models.CASCADE, related_name='posts', verbose_name='Категория')
    title = models.CharField(max_length=512, unique=True, verbose_name='Наименование')
    image = models.ImageField(upload_to='posts', blank=True, verbose_name='Изображение')
    tags = models.CharField(max_length=256, blank=True, verbose_name='Тэги')
    body = models.TextField(verbose_name='Текст Хаба')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Хаб'
        verbose_name_plural = 'Хабы'

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def publish(self):
        self.is_published = True
        self.save()

    def get_links(self):
        return self.links.select_related()

    def get_publish_status(self):
        if self.is_published:
            return 'Опубликован'
        return 'Не опубликован'


class Links(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid4)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='links', verbose_name='Хаб')
    name = models.CharField(max_length=128, verbose_name='Наименование')
    link = models.URLField(verbose_name='Ссылка')
