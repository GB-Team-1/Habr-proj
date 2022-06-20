from django.conf import settings
from django.core.mail import send_mail


def send_notification(notify):
    message = 'Notify!!!'

    return send_mail(
        'Уведомление с портала...',
        message,
        settings.EMAIL_HOST_USER,
        [notify.to_user],
        fail_silently=False
    )
