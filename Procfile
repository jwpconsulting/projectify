release: ./manage.py migrate --noinput
web: newrelic-admin run-program gunicorn projectify.asgi -w 3 -b "0.0.0.0:$PORT" -k uvicorn.workers.UvicornWorker
worker: newrelic-admin run-program celery -A projectify worker -c 1
