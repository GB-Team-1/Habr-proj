from django.urls import path

from subscribe.views import SubscribeView, UnSubscribeView, FollowersView, SubscribesView

app_name = 'subscribe'

urlpatterns = [
    path('subscribes/<pk>/', SubscribeView.as_view(), name='subscribes'),
    path('unsubscribes/<pk>/', UnSubscribeView.as_view(), name='unsubscribes'),

    path('followers/<pk>/', FollowersView.as_view(), name='followers'),
    path('view_subscribes/<pk>/', SubscribesView.as_view(), name='view_subscribes'),
]
