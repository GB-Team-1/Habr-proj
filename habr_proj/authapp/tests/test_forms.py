from django.core.exceptions import ValidationError
from django.test import TestCase

from authapp.forms import HabrUserLoginForm, HabrUserRegisterForm
from authapp.models import HabrUser


class HabrUserLoginFormTest(TestCase):
    def test_username_field_label(self):
        form = HabrUserLoginForm()
        self.assertTrue(form.fields['username'].label is None or form.fields['username'].label == 'Имя пользователя')

    def test_password_field_label(self):
        form = HabrUserLoginForm()
        self.assertTrue(form.fields['password'].label is None or form.fields['password'].label == 'Пароль')


class HabrUserRegisterFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        HabrUser.objects.create_user(username='test_user', email='test@test.com',
                                     password='test123456')
        cls.form_data = {
            'username': 'test1',
            'email': 'user@test.com',
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'password1': 'user123456',
            'password2': 'user123456'
        }

    def test_username_field_label(self):
        form = HabrUserRegisterForm()
        self.assertTrue(form.fields['username'].label is None or form.fields['username'].label == 'Имя пользователя')

    def test_firstname_field_label(self):
        form = HabrUserRegisterForm()
        self.assertTrue(form.fields['first_name'].label is None or form.fields['first_name'].label == 'Имя')

    def test_lastname_field_label(self):
        form = HabrUserRegisterForm()
        self.assertTrue(form.fields['last_name'].label is None or form.fields['last_name'].label == 'Фамилия')

    def test_email_field_label(self):
        form = HabrUserRegisterForm()
        self.assertTrue(form.fields['email'].label is None or form.fields['email'].label == 'Адрес электронной почты')

    def test_password1_field_label(self):
        form = HabrUserRegisterForm()
        self.assertTrue(form.fields['password1'].label is None or form.fields['password1'].label == 'Пароль')

    def test_password2_field_label(self):
        form = HabrUserRegisterForm()
        self.assertTrue(form.fields['password2'].label is None or form.fields['password2'].label == 'Подтверждение пароля')

    def test_clean_valid_data(self):
        form = HabrUserRegisterForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_clean_not_valid_email(self):
        email = 'test@test.com'
        self.form_data['email'] = email
        form = HabrUserRegisterForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_clean_not_valid_username(self):
        username = 'test_user'
        self.form_data['username'] = username
        form = HabrUserRegisterForm(data=self.form_data)
        self.assertRaises(ValidationError)

    def test_clean_not_valid_password(self):
        password2 = 'user1234567'
        self.form_data['password2'] = password2
        form = HabrUserRegisterForm(data=self.form_data)
        self.assertRaises(ValidationError)

    def test_save_form(self):
        form = HabrUserRegisterForm(data=self.form_data)
        form.save()
        user = HabrUser.objects.get(username=self.form_data['username'])
        self.assertFalse(user.is_active)
