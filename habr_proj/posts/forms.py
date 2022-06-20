from django import forms

from posts.models import Posts, Links, Comment


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Posts
        exclude = ('uid', 'created_at', 'updated_at', 'is_active', 'user')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'is_published':
                field.widget.attrs['class'] = 'colorinput-color bg-primary'
            else:
                field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Posts
        exclude = ('uid', 'created_at', 'updated_at', 'is_active', 'user')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'is_published':
                field.widget.attrs['class'] = 'colorinput-color bg-primary'
            else:
                field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_body(self):
        data = self.cleaned_data['body']
        if 'script' in data:
            raise forms.ValidationError('Нельзя использовать script на странице')
        return data


class LinksCreateForm(forms.ModelForm):
    class Meta:
        model = Links
        fields = ('name', 'link',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_body',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_body',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

