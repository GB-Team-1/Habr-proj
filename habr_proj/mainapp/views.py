from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from notifyapp.views import get_all_notify, get_all_unread_notify
from posts.models import PostCategory, Posts
from posts.views import get_categories


class Index(ListView):
    model = Posts
    template_name = 'mainapp/index.html'
    paginate_by = 6

    def get_queryset(self):
        return Posts.objects.filter(is_published=True, is_active=True, is_moderated=True,
                                    status_moderation=Posts.POST_MODERATE).order_by('-created_at').select_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        context['categories'] = get_categories()
        context['notify'] = get_all_notify(pk=self.request.user.pk)[:5]
        context['notify_count'] = get_all_unread_notify(pk=self.request.user.pk)
        return context


class SearchView(ListView):
    model = Posts
    template_name = 'mainapp/seacrh.html'

    def get_queryset(self):
        query = self.request.GET.get('search')
        queryset = Posts.objects.filter(
            (Q(title__icontains=query) | Q(body__icontains=query)) & Q(is_published=True) & Q(is_active=True) & Q(
                is_moderated=True) & Q(status_moderation=Posts.POST_MODERATE)).order_by('-created_at').select_related()
        print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['title'] = 'Результат поиска'
        context['result'] = self.request.GET.get('search')
        return context
