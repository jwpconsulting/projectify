release: ./manage.py migrate --noinput
web: newrelic-admin run-program gunicorn projectify.wsgi -w 3 -b "0.0.0.0:$PORT"
