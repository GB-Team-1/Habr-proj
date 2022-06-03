from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, ListView

from posts.forms import PostCreateForm
from posts.models import Posts


class PostCreateView(CreateView):
    model = Posts
    form_class = PostCreateForm

    def get_success_url(self):
        return reverse('posts:list', args=[self.kwargs['pk']])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['title'] = 'Хаб/создание'
        return context_data


class PostListView(ListView):
    pass
