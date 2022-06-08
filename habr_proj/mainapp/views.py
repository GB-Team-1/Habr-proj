from django.shortcuts import render
from django.views.generic import TemplateView

from posts.models import PostCategory, Posts
from posts.views import get_categories


class Index(TemplateView):
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        context['categories'] = get_categories()
        context['posts'] = Posts.objects.filter(is_published=True).order_by('-created_at')
        return context


# class AllPostsView(TemplateView):
