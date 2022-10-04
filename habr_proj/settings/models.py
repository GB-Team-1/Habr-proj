from ckeditor.fields import RichTextField
from django.db import models


# Create your models here.


class Help(models.Model):
    title = models.CharField(max_length=512, unique=True, verbose_name='Наименование')
    body = RichTextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        verbose_name = 'Раздел помощь'
        verbose_name_plural = 'Раздел помощь'

