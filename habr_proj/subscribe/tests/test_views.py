from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from authapp.models import HabrUser
from subscribe.models import SubscribeModel


class SubscribeViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user1 = HabrUser.objects.create_user(username='test_user1', email='test1@test.com',
                                                  password='test123456', is_active=True)
        self.user2 = HabrUser.objects.create_user(username='test_user2', email='test2@test.com',
                                                  password='test123456', is_active=True)
        self.auth_user = self.client.login(username='test_user1', password='test123456')
        # self.subscribe = SubscribeModel.objects.create(user=self.user1, subscriber=self.user2)

    def test_subscribe_view(self):
        response = self.client.post(reverse('subscribe:subscribes', kwargs={'pk': self.user2.pk}))
        self.assertEqual(response.status_code, 302)
        sub = SubscribeModel.objects.all().first()
        self.assertEqual(sub.user, self.user2)
        self.assertEqual(sub.subscriber, self.user1)


class UnSubscribeViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user1 = HabrUser.objects.create_user(username='test_user1', email='test1@test.com',
                                                  password='test123456', is_active=True)
        self.user2 = HabrUser.objects.create_user(username='test_user2', email='test2@test.com',
                                                  password='test123456', is_active=True)
        self.auth_user = self.client.login(username='test_user1', password='test123456')
        self.subscribe = SubscribeModel.objects.create(user=self.user2, subscriber=self.user1)

    def test_unsubscribe_view(self):
        response = self.client.post(reverse('subscribe:unsubscribes', kwargs={'pk': self.user2.pk}))
        self.assertEqual(response.status_code, 302)
        sub = SubscribeModel.objects.all().first()
        self.assertEqual(sub, None)


class FollowersViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user1 = HabrUser.objects.create_user(username='test_user1', email='test1@test.com',
                                                  password='test123456', is_active=True)
        self.user2 = HabrUser.objects.create_user(username='test_user2', email='test2@test.com',
                                                  password='test123456', is_active=True)
        self.auth_user = self.client.login(username='test_user1', password='test123456')
        self.subscribe = SubscribeModel.objects.create(user=self.user2, subscriber=self.user1)

    def test_followers_list_view(self):
        response = self.client.get(reverse('subscribe:followers', kwargs={'pk': self.user2.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SubscribeModel.objects.filter(user=self.user2).count(), response.context['followers'].count())


class SubscribesViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user1 = HabrUser.objects.create_user(username='test_user1', email='test1@test.com',
                                                  password='test123456', is_active=True)
        self.user2 = HabrUser.objects.create_user(username='test_user2', email='test2@test.com',
                                                  password='test123456', is_active=True)
        self.auth_user = self.client.login(username='test_user1', password='test123456')
        self.subscribe = SubscribeModel.objects.create(user=self.user2, subscriber=self.user1)

    def test_followers_list_view(self):
        response = self.client.get(reverse('subscribe:view_subscribes', kwargs={'pk': self.user1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SubscribeModel.objects.filter(subscriber=self.user1).count(),  response.context['subscribes'].count())
