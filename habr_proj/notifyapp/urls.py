from django.urls import path

from notifyapp.views import NotifyConfirmAllView, NotifyListView, NotifyReadView, NotifyDeleteView

app_name = 'notify'

urlpatterns = [
    path('allconfirm/', NotifyConfirmAllView.as_view(), name='confirm_all'),
    path('list/', NotifyListView.as_view(), name='notify_list'),
    path('read/<category>/<pk>/', NotifyReadView.as_view(), name='notify_read'),
    path('delete/<category>/<pk>/', NotifyDeleteView.as_view(), name='notify_delete')
]
