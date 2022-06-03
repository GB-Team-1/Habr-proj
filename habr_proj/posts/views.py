from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from posts.models import Posts


class PostCreateView(CreateView):
    model = Posts
    fields = []
    success_url = reverse_lazy('posts:list')


class PostListView(ListView):
    pass
