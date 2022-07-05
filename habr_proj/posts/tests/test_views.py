from django.test import TestCase
from django.urls import reverse
from django.test.client import Client
from authapp.models import HabrUser
from posts.models import PostCategory, Posts, Comment


class PostCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = HabrUser.objects.create_user(username='test_user', email='test@test.com',
                                                 password='test123456', is_active=True)
        self.auth_user = self.client.login(username='test_user', password='test123456')
        self.category = PostCategory.objects.create(name='Маркетинг')
        self.form_data_post = {
            'user': self.user,
            'category': self.category,
            'title': 'Test1',
            'body': 'Test Body'
        }

    def test_create_post_view(self):
        response = self.client.get(reverse('posts:post_create'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('posts:post_create'), data=self.form_data_post)
        self.assertEqual(response.status_code, 200)


class PostListViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = HabrUser.objects.create_user(username='test_user', email='test@test.com',
                                                 password='test123456', is_active=True)
        self.auth_user = self.client.login(username='test_user', password='test123456')
        self.category = PostCategory.objects.create(name='Маркетинг')
        for i in range(10):
            Posts.objects.create(user=self.user, category=self.category, title=f'Test{i}', body=f'Test Body {i}')

    def test_list_post_view(self):
        response = self.client.get(reverse('posts:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('posts_list' in response.context)


class PostDeleteViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = HabrUser.objects.create_user(username='test_user', email='test@test.com',
                                                 password='test123456', is_active=True)
        self.auth_user = self.client.login(username='test_user', password='test123456')
        self.category = PostCategory.objects.create(name='Маркетинг')
        self.post = Posts.objects.create(user=self.user, category=self.category, title='Test', body='Test Body')

    def test_delete_post_view(self):
        response = self.client.get(reverse('posts:post_delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('posts:post_delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)
        new_post = Posts.objects.get(pk=self.post.pk)
        self.assertEqual(new_post.is_active, False)


class PostUpdateViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = HabrUser.objects.create_user(username='test_user', email='test@test.com',
                                                 password='test123456', is_active=True)
        self.auth_user = self.client.login(username='test_user', password='test123456')
        self.category = PostCategory.objects.create(name='Маркетинг')
        self.post = Posts.objects.create(user=self.user, category=self.category, title='Test', body='Test Body')

    def test_update_post_view(self):
        response = self.client.get(reverse('posts:post_update', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        data = {
            'user': self.user,
            'category': self.category,
            'title': 'Test',
            'body': 'New Test Body'
        }
        response = self.client.post(reverse('posts:post_update', kwargs={'pk': self.post.pk}), data)
        self.assertEqual(response.status_code, 200)


class PostPublishViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = HabrUser.objects.create_user(username='test_user', email='test@test.com',
                                                 password='test123456', is_active=True)
        self.auth_user = self.client.login(username='test_user', password='test123456')
        self.category = PostCategory.objects.create(name='Маркетинг')
        self.post = Posts.objects.create(user=self.user, category=self.category, title='Test', body='Test Body')

    def test_publish_post_view(self):
        new_post = self.post
        self.assertEqual(new_post.is_published, False)
        response = self.client.get(reverse('posts:post_publish', kwargs={'pk': new_post.pk}))
        new_post.refresh_from_db()
        self.assertEqual(new_post.is_published, True)


class PostDetailViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = HabrUser.objects.create_user(username='test_user', email='test@test.com',
                                                 password='test123456', is_active=True)
        self.auth_user = self.client.login(username='test_user', password='test123456')
        self.category = PostCategory.objects.create(name='Маркетинг')
        self.post = Posts.objects.create(user=self.user, category=self.category, title='Test', body='Test Body')

    def test_detail_post_view(self):
        response = self.client.get(reverse('posts:post_detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)


class PostListCategoryViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = HabrUser.objects.create_user(username='test_user', email='test@test.com',
                                                 password='test123456', is_active=True)
        self.auth_user = self.client.login(username='test_user', password='test123456')
        for i in range(5):
            category = PostCategory.objects.create(name=f'{i}')
            Posts.objects.create(user=self.user, category=category, title=f'Test{i}', body='Test Body')

    def test_category_list_view(self):
        categories = PostCategory.objects.all()
        for item in categories:
            response = self.client.get(reverse('posts:post_category', kwargs={'pk': item.pk}))
            self.assertEqual(response.status_code, 200)
            self.assertTrue('posts_list' in response.context)


class PostModerateListViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = HabrUser.objects.create_user(username='test_user', email='test@test.com',
                                                 password='test123456', is_active=True)
        self.auth_user = self.client.login(username='test_user', password='test123456')
        self.category = PostCategory.objects.create(name='Маркетинг')
        self.post = Posts.objects.create(user=self.user, category=self.category, title='Test', body='Test Body')

    def test_moderate_list_view(self):
        response = self.client.get(reverse('posts:moderate_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('posts_list' in response.context)


class CommentDeleteViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = HabrUser.objects.create_user(username='test_user', email='test@test.com',
                                                 password='test123456', is_active=True)
        self.auth_user = self.client.login(username='test_user', password='test123456')
        self.category = PostCategory.objects.create(name='Маркетинг')
        self.post = Posts.objects.create(user=self.user, category=self.category, title='Test', body='Test Body')
        self.comment = Comment.objects.create(user=self.user, post=self.post, comment_body='Test')

    def test_delete_comment_view(self):
        response = self.client.get(reverse('posts:comment_delete', kwargs={'pk': self.comment.pk}))
        self.assertEqual(response.status_code, 302)
        new_comment = Comment.objects.get(pk=self.comment.pk)
        self.assertEqual(new_comment.is_active, False)


class CommentUpdateViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = HabrUser.objects.create_user(username='test_user', email='test@test.com',
                                                 password='test123456', is_active=True)
        self.auth_user = self.client.login(username='test_user', password='test123456')
        self.category = PostCategory.objects.create(name='Маркетинг')
        self.post = Posts.objects.create(user=self.user, category=self.category, title='Test', body='Test Body')
        self.comment = Comment.objects.create(user=self.user, post=self.post, comment_body='Test')

    def test_update_comment_view(self):
        data = {
            'comment_body':'Test new'
        }
        response = self.client.post(reverse('posts:comment_update', kwargs={'pk': self.comment.pk}), data=data)
        self.assertEqual(response.status_code, 302)
        new_comment = Comment.objects.get(pk=self.comment.pk)
        self.assertEqual(new_comment.comment_body, data['comment_body'])



