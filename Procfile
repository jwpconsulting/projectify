release: ./manage.py migrate --noinput
web: daphne projectify.asgi:application -b 0.0.0.0 -p $PORT
worker: celery -A projectify worker -c 1
