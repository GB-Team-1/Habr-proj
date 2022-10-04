from django.test import TestCase

from authapp.models import HabrUser


class HabrUserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        HabrUser.objects.create_user(username='test_user', email='test@test.com',
                                     password='test123456', is_active=False)

    def test_avatar_label(self):
        user = HabrUser.objects.all().first()
        field_label = user._meta.get_field('avatar').verbose_name
        self.assertEqual(field_label, 'Аватар')

    def test_birthday_label(self):
        user = HabrUser.objects.all().first()
        field_label = user._meta.get_field('birthday').verbose_name
        self.assertEqual(field_label, 'Дата рождения')

    def test_about_me_label(self):
        user = HabrUser.objects.all().first()
        field_label = user._meta.get_field('about_me').verbose_name
        self.assertEqual(field_label, 'Обо мне')

    def test_specialization_label(self):
        user = HabrUser.objects.all().first()
        field_label = user._meta.get_field('specialization').verbose_name
        self.assertEqual(field_label, 'Специализация')

    def test_about_me_max_length(self):
        user = HabrUser.objects.all().first()
        max_length = user._meta.get_field('about_me').max_length
        self.assertEqual(max_length, 512)

    def test_specialization_max_length(self):
        user = HabrUser.objects.all().first()
        max_length = user._meta.get_field('specialization').max_length
        self.assertEqual(max_length, 150)

    def test_activate_user(self):
        user = HabrUser.objects.all().first()
        self.assertEqual(user.is_active, False)
        user.activate_user()
        self.assertEqual(user.is_active, True)
