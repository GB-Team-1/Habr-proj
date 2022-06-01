from django.core.management.base import BaseCommand
from django.conf import settings
from faker import Faker

from authapp.models import HabrUser
from posts.models import PostCategory

fake = Faker()

class Command(BaseCommand):
    def handle(self, *args, **options):
        HabrUser.objects.all().delete()
        HabrUser.objects.create_superuser(
            settings.ADMIN_USERNAME,
            email=settings.ADMIN_EMAIL,
            password=settings.ADMIN_PASSWORD
        )
        PostCategory.objects.all().delete()
        PostCategory.objects.create(name='design').save()
        PostCategory.objects.create(name='web').save()
        PostCategory.objects.create(name='mobile').save()
        PostCategory.objects.create(name='marketing').save()
