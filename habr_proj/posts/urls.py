from django.urls import path

from posts.views import PostCreateView, PostListView

app_name = 'posts'

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('list/<pk>/', PostListView.as_view(), name='post_list'),
]
