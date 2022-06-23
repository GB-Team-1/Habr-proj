from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from settings.models import Help


class HelpView(TemplateView):
    template_name = 'settings/help.html'

    def get_context_data(self, **kwargs):
        context = super(HelpView, self).get_context_data(**kwargs)
        context['title'] = 'Помощь'
        context['help_title'] = Help.objects.all()
        return context