from django.urls import path

from notifyapp.views import NotifyConfirmAllView, NotifyListView, NotifyDetailView, NotifyDeleteView

app_name = 'notify'

urlpatterns = [
    path('allconfirm/', NotifyConfirmAllView.as_view(), name='confirm_all'),
    path('list/', NotifyListView.as_view(), name='notify_list'),
    path('detail/<pk>/', NotifyDetailView.as_view(), name='notify_detail'),
    path('delete/<pk>/', NotifyDeleteView.as_view(), name='notify_delete')
]
