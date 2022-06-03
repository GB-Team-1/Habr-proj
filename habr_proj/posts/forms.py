from django import forms

from posts.models import Posts


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Posts
        exclude = ('uid', 'created_at', 'updated_at', 'is_active',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
