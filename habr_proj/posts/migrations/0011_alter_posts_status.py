# Generated by Django 3.2.8 on 2022-06-21 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_auto_20220621_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='status',
            field=models.CharField(choices=[('TO', 'На модерации'), ('PM', 'Одобрен'), ('PUB', 'Опубликован'), ('BLC', 'Заблокирован'), ('NPUB', 'Не опубликован')], default='TO', max_length=10, verbose_name='Статус хаба'),
        ),
    ]
