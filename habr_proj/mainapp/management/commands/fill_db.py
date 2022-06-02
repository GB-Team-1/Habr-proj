from django.core.management.base import BaseCommand
from django.conf import settings
from faker import Faker

from authapp.models import HabrUser
from posts.models import PostCategory

fake = Faker()

class Command(BaseCommand):
    def handle(self, *args, **options):
        HabrUser.objects.create_superuser(
            username=settings.ADMIN_USERNAME,
            email=settings.ADMIN_EMAIL,
            password=settings.ADMIN_PASSWORD
        )
        PostCategory.objects.all().delete()
        PostCategory.objects.create(name='Дизайн').save()
        PostCategory.objects.create(name='Веб-разработка').save()
        PostCategory.objects.create(name='Мобильная разработка').save()
        PostCategory.objects.create(name='Маркетинг').save()
