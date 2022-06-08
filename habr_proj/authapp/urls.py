from django.urls import path

from authapp.views import LoginUserView, LogoutUserView, RegisterUserView, VerifyUserView, UpdateProfileView
from posts.views import PostDetailProfileView

app_name = 'authapp'

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify/<key>/', VerifyUserView.as_view(), name='verify'),
    path('verify/<key>/', VerifyUserView.as_view(), name='verify'),
    path('profile/', UpdateProfileView.as_view(), name='profile'),

    path('profile/post-detail/<pk>/', PostDetailProfileView.as_view(), name='post_detail_profile')
]
