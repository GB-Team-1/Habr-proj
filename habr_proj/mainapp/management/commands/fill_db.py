from django.core.management.base import BaseCommand
from django.conf import settings
from faker import Faker

from authapp.models import HabrUser

fake = Faker()

class Command(BaseCommand):
    def handle(self, *args, **options):
        HabrUser.objects.all().delete()
        HabrUser.objects.create_superuser(
            settings.ADMIN_USERNAME,
            email=settings.ADMIN_EMAIL,
            password=settings.ADMIN_PASSWORD
        )
        for i in range(int(input('Введите количество пользователей: '))):
            user = HabrUser.objects.create(
                username=fake.name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                birthday=fake.date_of_birth(),
                about_me=fake.sentence(nb_words=10, variable_nb_words=True)
            )
            user.save()
