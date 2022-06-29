from authapp.models import HabrUser
from authapp.services import send_verify_email
from habr_proj.celery import app


@app.task
def send_verify_email_task(user_id):
    try:
        user = HabrUser.objects.get(pk=user_id)
        send_verify_email(user)
    except HabrUser.DoesNotExist:
        print(f'Пользователь с uid {user_id} не существует')
