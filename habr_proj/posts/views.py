from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView

from posts.forms import PostCreateForm, CommentCreateForm, PostUpdateForm, CommentUpdateForm
from posts.models import Posts, PostCategory, Comment, PostsLikes


def get_posts_in_category(pk):
    if settings.LOW_CACHE:
        key = 'posts_in_category'
        posts_in_category = cache.get(key)
        if posts_in_category is None:
            posts_in_category = Posts.objects.filter(category__pk=pk,
                                                     is_active=True,
                                                     is_published=True,
                                                     is_moderated=True,
                                                     status_moderation=Posts.POST_MODERATE
                                                     ).select_related().order_by('-created_at')
            cache.set(key, posts_in_category)
        return posts_in_category
    return Posts.objects.filter(category__pk=pk, is_active=True, is_published=True, is_moderated=True,
                                status_moderation=Posts.POST_MODERATE).select_related().order_by('-created_at')


def get_categories():
    if settings.LOW_CACHE:
        key = 'post_category'
        post_category = cache.get(key)
        if post_category is None:
            post_category = PostCategory.objects.all()
            cache.set(key, post_category)
        return post_category
    return PostCategory.objects.all()


def get_comments(pk):
    return Comment.objects.filter(post__pk=pk, is_active=True).order_by('-created_at')


class PostCreateView(LoginRequiredMixin, CreateView):
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


class PostListView(LoginRequiredMixin, ListView):
    model = Posts

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user, is_active=True).order_by(
            '-created_at').select_related()

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = f'Хабы {self.request.user}'
        context_data['categories'] = get_categories()

        return context_data


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Posts
    success_url = reverse_lazy('posts:post_list')


class PostUpdateView(LoginRequiredMixin, UpdateView):
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


class PostPublishView(LoginRequiredMixin, DetailView):

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
        context_data['comments'] = get_comments(self.kwargs.get('pk'))
        return context_data

    def post(self, request, *args, **kwargs):
        reverse_param = reverse('posts:post_detail', kwargs={'pk': self.kwargs.get('pk')})
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect('%s?next=%s' % (reverse('auth:login'), reverse_param))
        form = self.get_form()
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.post = self.get_queryset()[0]
            user.save()
            return HttpResponseRedirect(reverse_param)
        return super(PostDetailView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.get_queryset().first()
        post.views = F('views') + 1
        post.save()
        return super().get(request, *args, **kwargs)


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


class PostModerateView(LoginRequiredMixin, DetailView):

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


class PostModerateListView(LoginRequiredMixin, ListView):
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


class CommentDeleteView(LoginRequiredMixin, DetailView):
    model = Comment

    def get_queryset(self):
        return Comment.objects.filter(pk=self.kwargs.get('pk')).first()

    def get(self, request, *args, **kwargs):
        comment = self.get_queryset()
        comment.is_active = False
        comment.save()
        return HttpResponseRedirect(reverse('posts:post_detail', kwargs={'pk': comment.post.pk}))


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    form_class = CommentUpdateForm
    template_name = 'posts/post_detail.html'

    def get_queryset(self):
        return Comment.objects.filter(pk=self.kwargs.get('pk'))

    def get_success_url(self):
        comment = self.get_queryset().first()
        return reverse_lazy('posts:post_detail', kwargs={'pk': comment.post.pk})


@login_required(login_url='/auth/login/')
def like_or_dislike(request, pk):
    if request.is_ajax():
        post = Posts.objects.get(pk=pk)
        like = PostsLikes.objects.filter(for_post=post, user=request.user).first()
        if like:
            if like.is_like:
                print('DISLIKE')
                like.is_like = False
                post.post_like.remove(request.user)
            else:
                print('LIKE')
                like.is_like = True
                post.post_like.add(request.user)
            post.save()
            like.save()
        else:
            PostsLikes.objects.create(for_post=post, user=request.user)
        like = PostsLikes.objects.filter(for_post=post, user=request.user).first()
        return JsonResponse({
            'is_like': like.is_like,
            'likes': post.get_likes_quantity()
        })
