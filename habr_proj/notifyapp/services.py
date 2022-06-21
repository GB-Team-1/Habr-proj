from django.conf import settings
from django.core.mail import send_mail


def send_notification(notify):
    message = notify.notify_body

    return send_mail(
        'Уведомление с портала...',
        message,
        settings.EMAIL_HOST_USER,
        [notify.to_user.email],
        fail_silently=False
    )
