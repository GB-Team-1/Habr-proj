from django.urls import path

from posts import views as posts
from posts.views import PostListCategoryView, CommentDeleteView, CommentUpdateView, PostModerateView

app_name = 'posts'

urlpatterns = [
    path('create/', posts.PostCreateView.as_view(), name='post_create'),
    path('list/', posts.PostListView.as_view(), name='post_list'),
    path('delete/<pk>/', posts.PostDeleteView.as_view(), name='post_delete'),
    path('update/<pk>/', posts.PostUpdateView.as_view(), name='post_update'),
    path('publish/<pk>/', posts.PostPublishView.as_view(), name='post_publish'),

    path('detail/<pk>/', posts.PostDetailView.as_view(), name='post_detail'),
    path('category/<pk>/', PostListCategoryView.as_view(), name='post_category'),

    path('comment/delete/<pk>/', CommentDeleteView.as_view(), name='comment_delete'),
    path('comment/update/<pk>/', CommentUpdateView.as_view(), name='comment_update'),

    path('moderate/<pk>/<mod_result>/', PostModerateView.as_view(), name='post_moderate')
]
