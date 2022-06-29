from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView

from notifyapp.models import NotifyPostStatus
from notifyapp.services import send_notification
from posts.forms import PostCreateForm, CommentCreateForm, PostUpdateForm, CommentUpdateForm
from posts.models import Posts, PostCategory, Comment


def get_posts_in_category(pk):
    return Posts.objects.filter(category__pk=pk, is_active=True, is_published=True, is_moderated=True,
                                status_moderation=Posts.POST_MODERATE).select_related() \
        .order_by('-created_at')


def get_categories():
    # TODO Добавить кэширование
    return PostCategory.objects.all()


class PostCreateView(CreateView):
    model = Posts
    form_class = PostCreateForm
    template_name = 'posts/posts_form.html'
    success_url = reverse_lazy('posts:post_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Хаб/создание'
        context_data['create_update'] = 'Создание Хаба'
        context_data['create_update_text'] = 'создать новый'
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
        return super().get_queryset().filter(user=self.request.user, is_active=True).order_by(
            '-created_at').select_related()

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = f'Хабы {self.request.user}'
        context_data['categories'] = get_categories()

        return context_data


class PostDeleteView(DeleteView):
    model = Posts
    success_url = reverse_lazy('posts:post_list')


class PostUpdateView(UpdateView):
    model = Posts
    template_name = 'posts/posts_form_update.html'
    form_class = PostUpdateForm
    success_url = reverse_lazy('posts:post_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Хаб/редактирование'
        context_data['create_update'] = 'Редактирование Хаба'
        context_data['create_update_text'] = 'редактировать'
        context_data['pk'] = self.kwargs.get('pk')
        return context_data
    #
    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     if form.is_valid():
    #         user = form.save(commit=False)
    #         user.user = request.user
    #         # user.is_moderated = False
    #         # user.status_moderation = Posts.POST_MODERATE
    #         user.save()
    #         # return HttpResponseRedirect(reverse('posts:post_list'))
    #     return super(PostUpdateView, self).post(request, *args, **kwargs)


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


class PostDetailView(UpdateView):
    template_name = 'posts/post_detail.html'
    form_class = CommentCreateForm

    def get_queryset(self):
        return Posts.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Хаб'
        context_data['post'] = self.get_queryset().first()
        context_data['comment_title'] = 'Написать комментарий'
        context_data['comments'] = Comment.objects.filter(post__pk=self.kwargs.get('pk'), is_active=True).order_by(
            '-created_at')
        return context_data

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.post = self.get_queryset()[0]
            user.save()
            return HttpResponseRedirect(reverse('posts:post_detail', kwargs={'pk': self.kwargs.get('pk')}))
        return super(PostDetailView, self).post(request, *args, **kwargs)


class PostDetailProfileView(DetailView):
    template_name = 'posts/posts_detail_profile.html'

    def get_queryset(self):
        return Posts.objects.filter(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Хаб'
        context_data['post'] = self.get_queryset().first()
        return context_data


class PostListCategoryView(ListView):
    model = Posts
    template_name = 'posts/posts_category_list.html'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        category_pk = self.kwargs.get('pk')
        if category_pk != 0:
            queryset = get_posts_in_category(category_pk)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        category = PostCategory.objects.filter(pk=self.kwargs.get('pk'))[0]
        context_data['title'] = f'Хабы {category}'
        context_data['category_name'] = category
        context_data['categories'] = get_categories()

        return context_data


class PostModerateView(DetailView):

    def get_queryset(self):
        return Posts.objects.filter(pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        post = self.get_queryset().first()
        mod_result = self.kwargs.get('mod_result')
        if mod_result == 'ok':
            post.is_moderated = True
            post.status_moderation = 'PM'
            post.save()
        else:
            post.is_moderated = False
            post.status_moderation = 'BLC'
            post.save()
        return HttpResponseRedirect(reverse('posts:post_detail', kwargs={'pk': self.kwargs.get('pk')}))


class PostModerateListView(ListView):
    model = Posts
    template_name = 'posts/posts_moderate_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, is_moderated=False).order_by(
            '-created_at').select_related()

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = f'Хабы на модерацию'
        context_data['categories'] = get_categories()

        return context_data


class CommentDeleteView(DetailView):
    model = Comment

    def get_queryset(self):
        return Comment.objects.filter(pk=self.kwargs.get('pk')).first()

    def get(self, request, *args, **kwargs):
        comment = self.get_queryset()
        comment.is_active = False
        comment.save()
        return HttpResponseRedirect(reverse('posts:post_detail', kwargs={'pk': comment.post.pk}))


class CommentUpdateView(UpdateView):
    form_class = CommentUpdateForm
    template_name = 'posts/post_detail.html'

    def get_queryset(self):
        return Comment.objects.filter(pk=self.kwargs.get('pk'))

    def get_success_url(self):
        comment = self.get_queryset().first()
        return reverse_lazy('posts:post_detail', kwargs={'pk': comment.post.pk})
