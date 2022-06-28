from authapp.models import HabrUser
from habr_proj.celery import app
from notifyapp.models import NotifyPostStatus, NotifyComment, NotifyLike
from notifyapp.services import send_notification


@app.task
def send_notification_post(notify_id):
    try:
        notify = NotifyPostStatus.objects.get(pk=notify_id)
        send_notification(notify)
    except NotifyPostStatus.DoesNotExist:
        print(f'Объект уведомления с uid {notify_id} не существует')


@app.task
def send_notification_comment(notify_id):
    try:
        notify = NotifyComment.objects.get(pk=notify_id)
        send_notification(notify)
    except NotifyComment.DoesNotExist:
        print(f'Объект уведомления с uid {notify_id} не существует')


@app.task
def send_notification_like(notify_id):
    try:
        notify = NotifyLike.objects.get(pk=notify_id)
        send_notification(notify)
    except NotifyLike.DoesNotExist:
        print(f'Объект уведомления с uid {notify_id} не существует')


@app.task
def send_notification_user(notify_id):
    try:
        notify = HabrUser.objects.get(pk=notify_id)
        send_notification(notify)
    except HabrUser.DoesNotExist:
        print(f'Объект уведомления с uid {notify_id} не существует')
