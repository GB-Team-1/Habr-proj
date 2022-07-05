from django.test import TestCase
from authapp.models import HabrUser
from posts.forms import PostCreateForm, PostUpdateForm, CommentCreateForm
from posts.models import Posts, PostCategory, Comment


class PostCreateFormTest(TestCase):
    def setUp(self) -> None:
        self.user = HabrUser.objects.create_user(username='test_user', email='test@test.com',
                                                 password='test123456', is_active=True)
        self.category = PostCategory.objects.create(name='Маркетинг')
        self.post = Posts.objects.create(user=self.user, category=self.category, title='Test', body='Test Body')
        self.form_data_post = {
            'user': self.user,
            'category': self.category,
            'title': 'Test1',
            'body': 'Test Body'
        }

    def test_category_field_label(self):
        form = PostCreateForm()
        self.assertTrue(form.fields['category'].label is None or form.fields['category'].label == 'Категория')

    def test_title_field_label(self):
        form = PostCreateForm()
        self.assertTrue(form.fields['title'].label is None or form.fields['title'].label == 'Наименование')

    def test_image_field_label(self):
        form = PostCreateForm()
        self.assertTrue(form.fields['image'].label is None or form.fields['image'].label == 'Изображение')

    def test_tags_field_label(self):
        form = PostCreateForm()
        self.assertTrue(form.fields['tags'].label is None or form.fields['tags'].label == 'Тэги')

    def test_body_field_label(self):
        form = PostCreateForm()
        self.assertTrue(form.fields['body'].label is None or form.fields['body'].label == 'Текст Хаба')

    def test_is_published_field_label(self):
        form = PostCreateForm()
        self.assertTrue(form.fields['is_published'].label is None or form.fields['is_published'].label == 'Опубликован')

    def test_clean_data(self):
        form = PostCreateForm(data=self.form_data_post)
        self.assertTrue(form.is_valid())

    def test_not_valid_title_data(self):
        self.form_data_post['title'] = 'Test'
        form = PostCreateForm(data=self.form_data_post)
        self.assertFalse(form.is_valid())

    def test_not_valid_category_data(self):
        self.form_data_post['category'] = 'Test'
        form = PostCreateForm(data=self.form_data_post)
        self.assertFalse(form.is_valid())


class PostUpdateFormTest(TestCase):

    def test_category_field_label(self):
        form = PostUpdateForm()
        self.assertTrue(form.fields['category'].label is None or form.fields['category'].label == 'Категория')

    def test_title_field_label(self):
        form = PostUpdateForm()
        self.assertTrue(form.fields['title'].label is None or form.fields['title'].label == 'Наименование')

    def test_image_field_label(self):
        form = PostUpdateForm()
        self.assertTrue(form.fields['image'].label is None or form.fields['image'].label == 'Изображение')

    def test_tags_field_label(self):
        form = PostUpdateForm()
        self.assertTrue(form.fields['tags'].label is None or form.fields['tags'].label == 'Тэги')

    def test_body_field_label(self):
        form = PostUpdateForm()
        self.assertTrue(form.fields['body'].label is None or form.fields['body'].label == 'Текст Хаба')

    def test_is_published_field_label(self):
        form = PostUpdateForm()
        self.assertTrue(form.fields['is_published'].label is None or form.fields['is_published'].label == 'Опубликован')


class CommentCreateFormTest(TestCase):
    def setUp(self) -> None:
        self.user = HabrUser.objects.create_user(username='test_user', email='test@test.com',
                                                 password='test123456', is_active=True)
        self.category = PostCategory.objects.create(name='Маркетинг')
        self.post = Posts.objects.create(user=self.user, category=self.category, title='Test', body='Test Body')
        self.form_data = {
            'post': self.post,
            'user': self.user,
            'comment_body': 'test comment'
        }

    def test_comment_body_field_label(self):
        form = CommentCreateForm()
        self.assertTrue(form.fields['comment_body'].label is None or form.fields['comment_body'].label == 'Комментарий')

    def test_clean_data(self):
        form = CommentCreateForm(data=self.form_data)
        self.assertTrue(form.is_valid())


class CommentUpdateFormTest(TestCase):
    def test_comment_body_field_label(self):
        form = CommentCreateForm()
        self.assertTrue(form.fields['comment_body'].label is None or form.fields['comment_body'].label == 'Комментарий')
