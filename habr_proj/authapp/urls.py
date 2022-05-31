from django.urls import path

from authapp.views import LoginUserView, LogoutUserView, RegisterUserView, VerifyUserView

app_name = 'authapp'

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify/<key>/', VerifyUserView.as_view(), name='verify'),
]
