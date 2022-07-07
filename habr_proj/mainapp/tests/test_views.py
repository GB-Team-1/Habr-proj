from django.test import TestCase
from django.urls import reverse

from authapp.models import HabrUser
from posts.models import PostCategory, Posts


class IndexViewTest(TestCase):
    def setUp(self) -> None:
        category = PostCategory.objects.create(name='Дизайн')

        self.username = 'test_user5'
        self.password = 'test1234567'
        user = HabrUser.objects.create_user(username=self.username, email='test@test.com',
                                            password=self.password)

        for i in range(20):
            Posts.objects.create(
                category=category,
                user=user,
                title=f'Хаб № {i}',
                body='<p>Текст Хаба</p>',
                is_moderated=True,
                is_published=True,
                status_moderation=Posts.POST_MODERATE
            )

    def test_index_view(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

    def test_index_pagination(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['object_list']) == 6)

    def test_search_view(self):
        response = self.client.get(reverse('search'), data={'search': 'Хаб № 1'})
        self.assertEqual(response.status_code, 200)
