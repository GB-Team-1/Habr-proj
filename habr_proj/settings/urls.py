from django.urls import path

from settings.views import HelpView

app_name = 'settings'

urlpatterns = [
    path('help/', HelpView.as_view(), name='help'),
]
