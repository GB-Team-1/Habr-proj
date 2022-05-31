from django.urls import path

from authapp.views import LoginUserView, LogoutUserView

app_name = 'authapp'

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]
