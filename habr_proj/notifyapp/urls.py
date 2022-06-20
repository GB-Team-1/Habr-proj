from django.urls import path

from notifyapp.views import NotifyConfirmAllView

app_name = 'notify'

urlpatterns = [
    path('allconfirm/', NotifyConfirmAllView.as_view(), name='confirm_all')
]
