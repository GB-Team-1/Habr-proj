from django.contrib.auth.forms import AuthenticationForm

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
