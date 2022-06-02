# Generated by Django 3.2.8 on 2022-06-02 19:19

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=512, unique=True, verbose_name='Наименование')),
                ('image', models.ImageField(blank=True, upload_to='posts', verbose_name='Изображение')),
                ('tags', models.CharField(blank=True, max_length=256, verbose_name='Тэги')),
                ('body', models.TextField(verbose_name='Текст Хаба')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('is_published', models.BooleanField(default=False, verbose_name='Опубликован')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='posts.postcategory', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Хаб',
                'verbose_name_plural': 'Хабы',
            },
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, verbose_name='Наименование')),
                ('link', models.URLField(verbose_name='Ссылка')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='posts.posts', verbose_name='Хаб')),
            ],
        ),
    ]
