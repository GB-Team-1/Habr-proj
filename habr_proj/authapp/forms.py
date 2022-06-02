import datetime

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from authapp.models import HabrUser


class HabrUserLoginForm(AuthenticationForm):
    class Meta:
        model = HabrUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class HabrUserRegisterForm(UserCreationForm):
    class Meta:
        model = HabrUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(HabrUserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_email(self):
        data = self.cleaned_data['email']
        email_list = list(HabrUser.objects.values('email'))
        for i in email_list:
            if data == i.get('email'):
                raise forms.ValidationError('Такой email уже существует')

        return data

    def clean_username(self):
        data = self.cleaned_data['username']
        username_list = list(HabrUser.objects.values('username'))
        for i in username_list:
            if data == i.get('username'):
                raise forms.ValidationError('Такой ник уже существует')
        return data

    def clean_password(self):
        pass_1 = self.cleaned_data['password1']
        pass_2 = self.cleaned_data['password2']
        if pass_1 != pass_2:
            raise forms.ValidationError('Пароли не совпадают')
        return pass_1

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.is_active = False
        user.save()
        return user


class HabrUserEditForm(UserChangeForm):
    class Meta:
        model = HabrUser
        fields = ('username', 'first_name', 'last_name', 'email', 'birthday', 'about_me', 'password',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()
