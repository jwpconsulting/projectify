# Podman / Docker

This assumes that you are using [Podman](https://podman.io/). The three
commands

- projectify-backend,
- projectify-celery, and
- projectify-manage

can be built from the repository's root directory using

```bash
podman build -t projectify-backend:latest -f containers/projectify-backend.Dockerfile .
podman build -t projectify-celery:latest -f containers/projectify-celery.Dockerfile .
podman build -t projectify-manage:latest -f containers/projectify-manage.Dockerfile .
```

Try running projectify-manage using

```bash
podman run \
  --env-file backend/.env.production-sample \
  projectify-manage:latest \
  shell_plus -c 'print(settings.STATIC_ROOT)'
```

For the database, you can use sqlite. Create a [Podman volume](https://docs.podman.io/en/latest/markdown/podman-volume.1.html):

```fish
podman volume create projectify-backend-db
```

Try creating and migrating a database:

```fish
podman run \
  --rm \
  --interactive \
  --volume projectify-backend-db:/var/projectify/db \
  docker-archive:(zcat result | psub) manage.py seeddb
```

This will start a server:

```fish
podman run \
    --expose 8000 \
    --publish 8000:8000 \
  --volume projectify-backend-db:/var/projectify/db \
    --interactive \
    docker-archive:(zcat result | psub)
```
