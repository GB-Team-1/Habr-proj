from django.test import TestCase

from authapp.models import HabrUser
from notifyapp.models import NotifyPostStatus
from posts.models import PostCategory, Posts, Comment


class NotifyPostStatusTest(TestCase):
    def setUp(self) -> None:
        self.user1 = HabrUser.objects.create_user(username='test_user1', email='test1@test.com',
                                                  password='test123456', is_active=True)
        self.category = PostCategory.objects.create(name='Маркетинг')
        self.post = Posts.objects.create(user=self.user1, category=self.category, title='Test', body='Test Body')
        self.notif = NotifyPostStatus.objects.create(to_user=self.user1, post=self.post, notify_body='test')

    def test_notif_to_user_label(self):
        field_label = self.notif._meta.get_field('to_user').verbose_name
        self.assertEqual(field_label, 'Пользователю')

    def test_notif_post_label(self):
        field_label = self.notif._meta.get_field('post').verbose_name
        self.assertEqual(field_label, 'Хаб')

    def test_notif_notify_body_label(self):
        field_label = self.notif._meta.get_field('notify_body').verbose_name
        self.assertEqual(field_label, 'Содержание уведомления')

    def test_notif_status_send_label(self):
        field_label = self.notif._meta.get_field('status_send').verbose_name
        self.assertEqual(field_label, 'Статус отпраки')

    def test_notif_status_label(self):
        field_label = self.notif._meta.get_field('status').verbose_name
        self.assertEqual(field_label, 'Статус хаба')

    def test_notif_is_read_label(self):
        field_label = self.notif._meta.get_field('is_read').verbose_name
        self.assertEqual(field_label, 'Прочитано')

    def test_notif_to_moder_label(self):
        field_label = self.notif._meta.get_field('to_moder').verbose_name
        self.assertEqual(field_label, 'Для модератора')


class NotifyCommentTest(TestCase):
    def setUp(self) -> None:
        self.user1 = HabrUser.objects.create_user(username='test_user1', email='test1@test.com',
                                                  password='test123456', is_active=True)
        self.category = PostCategory.objects.create(name='Маркетинг')
        self.post = Posts.objects.create(user=self.user1, category=self.category, title='Test', body='Test Body')
        self.comment = Comment.objects.create(post=self.post, user=self.user1, comment_body='Test comment')
        self.notif = NotifyPostStatus.objects.create(to_user=self.user1, comment=self.comment, notify_body='test')

    def test_notif_to_user_label(self):
        field_label = self.notif._meta.get_field('to_user').verbose_name
        self.assertEqual(field_label, 'Пользователю')

    def test_notif_comment_label(self):
        field_label = self.notif._meta.get_field('comment').verbose_name
        self.assertEqual(field_label, 'Комментарий')

    def test_notif_notify_body_label(self):
        field_label = self.notif._meta.get_field('notify_body').verbose_name
        self.assertEqual(field_label, 'Содержание уведомления')

    def test_notif_status_send_label(self):
        field_label = self.notif._meta.get_field('status_send').verbose_name
        self.assertEqual(field_label, 'Статус отпраки')

    def test_notif_status_label(self):
        field_label = self.notif._meta.get_field('status').verbose_name
        self.assertEqual(field_label, 'Статус хаба')

    def test_notif_is_read_label(self):
        field_label = self.notif._meta.get_field('is_read').verbose_name
        self.assertEqual(field_label, 'Прочитано')

    def test_notif_to_moder_label(self):
        field_label = self.notif._meta.get_field('to_moder').verbose_name
        self.assertEqual(field_label, 'Для модератора')

