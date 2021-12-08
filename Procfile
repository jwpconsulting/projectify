release: ./manage.py migrate --noinput
web: newrelic-admin gunicorn projectify.wsgi -w 3 -b "0.0.0.0:$PORT"
