release: ./manage.py migrate --noinput
web: newrelic-admin run-program daphne projectify.asgi:application -b 0.0.0.0 -p $PORT
worker: newrelic-admin run-program celery -A projectify worker -c 1
