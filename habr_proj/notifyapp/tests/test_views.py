from django.test import TestCase
from django.urls import reverse
from django.test.client import Client

from authapp.models import HabrUser
from notifyapp.models import NotifyPostStatus
from posts.models import PostCategory, Posts


class NotifyConfirmAllViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user1 = HabrUser.objects.create_user(username='test_user1', email='test1@test.com',
                                                  password='test123456', is_active=True)
        self.auth_user = self.client.login(username='test_user1', password='test123456')
        self.category = PostCategory.objects.create(name='Маркетинг')
        self.post = Posts.objects.create(user=self.user1, category=self.category, title='Test', body='Test Body')
        self.notif = NotifyPostStatus.objects.create(to_user=self.user1, post=self.post, notify_body='test')

    def test_confirm_all_view(self):
        response = self.client.get(reverse('notify:confirm_all'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(NotifyPostStatus.objects.all().first().is_read)


class NotifyListViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user1 = HabrUser.objects.create_user(username='test_user1', email='test1@test.com',
                                                  password='test123456', is_active=True)
        self.auth_user = self.client.login(username='test_user1', password='test123456')
        self.category = PostCategory.objects.create(name='Маркетинг')
        self.post = Posts.objects.create(user=self.user1, category=self.category, title='Test', body='Test Body')
        self.notif = NotifyPostStatus.objects.create(to_user=self.user1, post=self.post, notify_body='test')

    def test_notif_list_view(self):
        response = self.client.get(reverse('notify:notify_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(NotifyPostStatus.objects.filter(to_user=self.user1).count(),
                         response.context['notify_list'].count())


class NotifyReadViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user1 = HabrUser.objects.create_user(username='test_user1', email='test1@test.com',
                                                  password='test123456', is_active=True)
        self.auth_user = self.client.login(username='test_user1', password='test123456')
        self.category = PostCategory.objects.create(name='Маркетинг')
        self.post = Posts.objects.create(user=self.user1, category=self.category, title='Test', body='Test Body')
        self.notif = NotifyPostStatus.objects.create(to_user=self.user1, post=self.post, notify_body='test',
                                                     category=NotifyPostStatus.CATEGORY_POST)

    def test_notif_read_view(self):
        response = self.client.get(
            reverse('notify:notify_read', kwargs={'category': NotifyPostStatus.CATEGORY_POST, 'pk': self.notif.pk}))
        self.assertEqual(response.status_code, 302)
        self.notif.refresh_from_db()
        self.assertTrue(self.notif.is_read)


class NotifyDeleteViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user1 = HabrUser.objects.create_user(username='test_user1', email='test1@test.com',
                                                  password='test123456', is_active=True)
        self.auth_user = self.client.login(username='test_user1', password='test123456')
        self.category = PostCategory.objects.create(name='Маркетинг')
        self.post = Posts.objects.create(user=self.user1, category=self.category, title='Test', body='Test Body')
        self.notif = NotifyPostStatus.objects.create(to_user=self.user1, post=self.post, notify_body='test',
                                                     category=NotifyPostStatus.CATEGORY_POST)

    def test_notif_read_view(self):
        response = self.client.get(
            reverse('notify:notify_delete', kwargs={'category': NotifyPostStatus.CATEGORY_POST, 'pk': self.notif.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(NotifyPostStatus.objects.filter(pk=self.notif.pk))
