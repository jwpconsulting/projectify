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
env DATABASE_URL="sqlite:////$PWD/projectify-backend.sqlite" \
    manage.py migrate
env DATABASE_URL="sqlite:////$PWD/projectify-backend.sqlite" \
    manage.py seeddb
```

Then run supervisord, which in turn will run all the relevant processes:

```bash
env REDIS_TLS_URL="redis://localhost:6379" \
    DATABASE_URL="sqlite:////$PWD/projectify-backend.sqlite" \
    supervisord -n
```
