from django.test import TestCase

from authapp.models import HabrUser


class LoginUserViewTest(TestCase):
    def setUp(self) -> None:
        self.username = 'test_user5'
        self.password = 'test1234567'
        HabrUser.objects.create_user(username=self.username, email='test@test.com',
                                     password=self.password, is_active=False)

    def test_view_user_is_not_active(self):
        response = self.client.post('/auth/login/', data={'username': self.username, 'password': self.password},
                                    follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_view_user_is_active(self):
        user = HabrUser.objects.get(username=self.username)
        user.is_active = True
        user.save()
        response = self.client.post('/auth/login/', data={'username': self.username, 'password': self.password},
                                    follow=True)
        self.assertTrue(response.context['user'].is_authenticated)


class LogoutUserViewTest(TestCase):
    def setUp(self) -> None:
        self.username = 'test_user5'
        self.password = 'test1234567'
        HabrUser.objects.create_user(username=self.username, email='test@test.com',
                                     password=self.password)

    def test_logout_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_authenticated)
        response = self.client.get('/auth/logout/')
        self.assertFalse(response.context['user'].is_authenticated)


class RegisterUserViewTest(TestCase):
    def setUp(self) -> None:
        self.credentials = {
            'username': 'test_user6',
            'password1': 'test1234567',
            'password2': 'test1234567',
            'email': 'user6@test.com'
        }

    def test_register_user(self):
        response = self.client.post('/auth/register/', data=self.credentials)
        self.assertTrue(response.url.startswith('/auth/login/'))
        self.assertTrue(HabrUser.objects.get(username=self.credentials['username']))


class VerifyUserViewTest(TestCase):
    def setUp(self) -> None:
        self.credentials = {
            'username': 'test_user6',
            'password1': 'test1234567',
            'password2': 'test1234567',
            'email': 'user6@test.com'
        }
        response = self.client.post('/auth/register/', data=self.credentials)

    def test_verify_user(self):
        user = HabrUser.objects.get(username=self.credentials['username'])
        response = self.client.get(f'/auth/verify/{user.uid}/')
        user = HabrUser.objects.get(username=self.credentials['username'])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.is_active)


class UpdateProfileViewTest(TestCase):
    def setUp(self) -> None:
        self.credentials = {
            'username': 'test_user6',
            'password': 'test1234567',
            'email': 'user6@test.com',
            'first_name': 'Ivan',
            'last_name': 'Ivanov'
        }
        HabrUser.objects.create_user(**self.credentials)

    def test_edit_profile_with_anonymous(self):
        self.credentials['last_name'] = 'Petrov'
        response = self.client.get('/auth/profile/', data=self.credentials)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/auth/login/'))

    def test_edit_profile_with_authenticated(self):
        self.credentials['last_name'] = 'Petrov'
        self.client.login(username=self.credentials['username'], password=self.credentials['password'])
        response = self.client.post('/auth/profile/', data=self.credentials)
        user = HabrUser.objects.get(username=self.credentials['username'])
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user.last_name, 'Petrov')


class UserProfileDetailViewTest(TestCase):
    def setUp(self) -> None:
        self.credentials = {
            'username': 'test_user6',
            'password': 'test1234567',
            'email': 'user6@test.com',
            'first_name': 'Ivan',
            'last_name': 'Ivanov'
        }
        self.user = HabrUser.objects.create_user(**self.credentials)

    def test_user_detail_view_anonymous(self):
        response = self.client.get(f'/auth/profile/{self.user.uid}/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/auth/login/'))

    def test_user_detail_with_authenticated(self):
        self.client.login(username=self.credentials['username'], password=self.credentials['password'])
        response = self.client.get(f'/auth/profile/{self.user.uid}/')
        self.assertEqual(response.status_code, 200)
