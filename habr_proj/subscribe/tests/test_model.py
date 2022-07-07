from django.test import TestCase

from authapp.models import HabrUser
from subscribe.models import SubscribeModel


class SubscribeModelTest(TestCase):
    def setUp(self) -> None:
        self.user1 = HabrUser.objects.create_user(username='test_user1', email='test1@test.com',
                                                 password='test123456', is_active=True)
        self.user2 = HabrUser.objects.create_user(username='test_user2', email='test2@test.com',
                                                 password='test123456', is_active=True)
        self.subscribe = SubscribeModel.objects.create(user=self.user1, subscriber=self.user2)

    def test_user_label(self):
        field_label = self.subscribe._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'Пользователь')

    def test_subscriber_label(self):
        field_label = self.subscribe._meta.get_field('subscriber').verbose_name
        self.assertEqual(field_label, 'Подписчик')
