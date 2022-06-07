from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView

from posts.forms import PostCreateForm
from posts.models import Posts


class PostCreateView(CreateView):
    model = Posts
    form_class = PostCreateForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Хаб/создание'
        return context_data

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            return HttpResponseRedirect(reverse('posts:post_list'))
        return super(PostCreateView, self).post(request, *args, **kwargs)


class PostListView(ListView):
    model = Posts

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user, is_active=True)


class PostDeleteView(DeleteView):
    model = Posts
    success_url = reverse_lazy('posts:post_list')


class PostUpdateView(UpdateView):
    pass


class PostPublishView(DetailView):

    def get_queryset(self):
        return Posts.objects.filter(pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        post = self.get_queryset().first()
        if post.is_published:
            post.is_published = False
            post.save()
        else:
            post.is_published = True
            post.save()
        return HttpResponseRedirect(reverse('posts:post_list'))

