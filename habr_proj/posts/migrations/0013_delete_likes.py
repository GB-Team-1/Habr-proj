# Generated by Django 3.2.8 on 2022-06-21 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_auto_20220621_1715'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Likes',
        ),
    ]
