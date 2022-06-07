from django.shortcuts import render
from django.views.generic import TemplateView

from posts.models import PostCategory, Posts


class Index(TemplateView):
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        context['categories'] = PostCategory.objects.filter()
        context['posts'] = Posts.objects.filter(is_published=True).order_by('-created_at')
        return context


# class AllPostsView(TemplateView):
