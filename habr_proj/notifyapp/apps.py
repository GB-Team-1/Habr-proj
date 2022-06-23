from django.apps import AppConfig


class NotifyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifyapp'

    def ready(self):
        import notifyapp.signals.handlers
