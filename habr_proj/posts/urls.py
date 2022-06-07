from django.urls import path

from posts import views as posts

app_name = 'posts'

urlpatterns = [
    path('create/', posts.PostCreateView.as_view(), name='post_create'),
    path('list/', posts.PostListView.as_view(), name='post_list'),
    path('delete/<pk>/', posts.PostDeleteView.as_view(), name='post_delete'),
    path('update/<pk>/', posts.PostUpdateView.as_view(), name='post_update'),
    path('publish/<pk>/', posts.PostPublishView.as_view(), name='post_publish')
]
