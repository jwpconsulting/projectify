# Projectify Supervisor

Use [Supervisor](http://supervisord.org/index.html) to conveniently launch
all processes as a regular user, without having to use systemd. This means
that supervisor will launch all of the below

- Projectify frontend
- Projectify backend
- Celery background worker
- Reverse proxy

This is useful for

- end-to-end testing Projectify
- verifying server configurations

Install all dependencies and activate the current folder's nix shell using

```bash
nix shell
```

It's recommended to use [direnv](https://direnv.net/) to automatically activate the shell.

```bash
direnv allow
```

Create and seed a database:

```bash
env DJANGO_SETTINGS_MODULE=projectify.settings.development \
    DJANGO_CONFIGURATION=DevelopmentNix \
    STATIC_ROOT=$PWD/static \
    DATABASE_URL="sqlite:////$PWD/projectify-backend.sqlite" \
    manage.py migrate
env DJANGO_SETTINGS_MODULE=projectify.settings.development \
    DJANGO_CONFIGURATION=DevelopmentNix \
    STATIC_ROOT=$PWD/static \
    DATABASE_URL="sqlite:////$PWD/projectify-backend.sqlite" \
    manage.py seeddb
env DJANGO_SETTINGS_MODULE=projectify.settings.development \
    DJANGO_CONFIGURATION=DevelopmentNix \
    STATIC_ROOT=$PWD/static \
    DATABASE_URL="sqlite:////$PWD/projectify-backend.sqlite" \
    manage.py collectstatic --noinput
```

Then run supervisord, which in turn will run all the relevant processes:

```bash
env DJANGO_SETTINGS_MODULE=projectify.settings.development \
    DJANGO_CONFIGURATION=DevelopmentNix \
    STATIC_ROOT=$PWD/static \
    PORT=8000 \
    DATABASE_URL="sqlite:////$PWD/projectify-backend.sqlite" \
    supervisord -n
env DJANGO_SETTINGS_MODULE=projectify.settings.development \
    DJANGO_CONFIGURATION=DevelopmentNix \
    STATIC_ROOT=$PWD/static \
    PORT=8000 \
    DATABASE_URL="sqlite:////$PWD/projectify-backend.sqlite" \
    gunicorn \
        --config ../backend/gunicorn.conf.py \
        --log-config ../backend/gunicorn-error.log
```
