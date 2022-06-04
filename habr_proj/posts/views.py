from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, ListView

from posts.forms import PostCreateForm
from posts.models import Posts


class PostCreateView(CreateView):
    model = Posts
    form_class = PostCreateForm

    # def get_success_url(self):
    #     return reverse('posts:list', args=[self.kwargs['pk']])

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
        return super(PostCreateView, self).post(request, *args, **kwargs)


class PostListView(ListView):
    pass
