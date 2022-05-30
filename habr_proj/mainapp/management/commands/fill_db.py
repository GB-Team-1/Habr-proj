from django.core.management.base import BaseCommand
from django.conf import settings

from authapp.models import HabrUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        HabrUser.objects.all().delete()
        HabrUser.objects.create_superuser(
            settings.ADMIN_USERNAME,
            email=settings.ADMIN_EMAIL,
            password=settings.ADMIN_PASSWORD
        )
