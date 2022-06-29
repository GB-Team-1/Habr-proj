# Habr-proj

Для функционирования сервиса отправки email необходимо:

1. Запустить контейнер с Redis командой docker run -p 6379:6379 --name some-redis -d redis

2. Запустить воркер командой celery -A habr_proj worker --loglevel=info  