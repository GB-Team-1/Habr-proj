from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from posts.models import PostCategory, Posts
from posts.views import get_categories


class Index(ListView):
    model = Posts
    template_name = 'mainapp/index.html'
    paginate_by = 6

    def get_queryset(self):
        return Posts.objects.filter(is_published=True, is_active=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        context['categories'] = get_categories()
        # context['posts'] = Posts.objects.filter(is_published=True, is_active=True).order_by('-created_at')
        return context


# class AllPostsView(TemplateView):
