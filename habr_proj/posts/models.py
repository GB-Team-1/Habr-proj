from uuid import uuid4

from ckeditor.fields import RichTextField
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
    POST_TO_MODERATION = 'TO'
    POST_MODERATE = 'PM'
    POST_BLOCKED = 'BLC'
    POST_MODERATE_STATUSES = (
        (POST_TO_MODERATION, 'На модерации'),
        (POST_MODERATE,  'Одобрен'),
        (POST_BLOCKED, 'Заблокирован'),
    )

    uid = models.UUIDField(primary_key=True, default=uuid4)
    user = models.ForeignKey(HabrUser, on_delete=models.CASCADE,
                             related_name='userpost', verbose_name='Пользователь', default=None)
    category = models.ForeignKey(PostCategory, on_delete=models.CASCADE, related_name='posts', verbose_name='Категория')
    title = models.CharField(max_length=512, unique=True, verbose_name='Наименование')
    image = models.ImageField(upload_to='posts', blank=True, verbose_name='Изображение')
    tags = models.CharField(max_length=256, blank=True, verbose_name='Тэги')
    body = RichTextField(verbose_name='Текст Хаба', )
    status_moderation = models.CharField(max_length=10, choices=POST_MODERATE_STATUSES,
                                         default=POST_TO_MODERATION, verbose_name='Статус модерации')
    views = models.BigIntegerField(default=0, verbose_name='Количество просмотров')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    is_moderated = models.BooleanField(default=False, verbose_name='Проверен')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    post_like = models.ManyToManyField(HabrUser, related_name='post_liked', blank=True)

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

    def get_comments_quantity(self):
        return Comment.objects.filter(post=self, is_active=True).count()

    def get_likes_quantity(self):
        return PostsLikes.objects.filter(for_post=self, is_like=True).count()

    def get_user_like(self):

        return self.post_like.all()


class Links(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid4)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='links', verbose_name='Хаб')
    name = models.CharField(max_length=128, verbose_name='Наименование')
    link = models.URLField(verbose_name='Ссылка')


class Comment(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid4)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, verbose_name='Хаб')
    user = models.ForeignKey(HabrUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    comment_body = RichTextField(verbose_name='Комментарий', default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class PostsLikes(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid4)
    user = models.ForeignKey(HabrUser, on_delete=models.CASCADE)
    for_post = models.ForeignKey(Posts, default=1, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True, verbose_name='Флаг лайк')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
