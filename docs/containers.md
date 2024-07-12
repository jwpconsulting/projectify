# Podman / Docker

This assumes that you are using [Podman](https://podman.io/). The three
commands

- projectify-backend,
- projectify-celery, and
- projectify-manage

can be built from the repository's root directory using the multi-stage build
Dockerfile in `containers/`

```bash
podman build --target projectify-backend --tag projectify-backend:latest --file projectify-backend.Dockerfile .
podman build --target projectify-celery --tag projectify-celery:latest --file projectify-backend.Dockerfile .
podman build --target projectify-manage --tag projectify-manage:latest --file projectify-backend.Dockerfile .
podman build --target projectify-frontend --tag projectify-frontend:latest --file projectify-frontend.Dockerfile .
podman build --target projectify-revproxy --tag projectify-revproxy:latest --file projectify-revproxy.Dockerfile .
```

Try running projectify-manage using

```bash
podman run \
  --env-file backend/.env.production-sample \
  projectify-manage:latest \
  shell_plus -c 'print(settings.STATIC_ROOT)'
```

This prints something like the following

```
[...]
from django.utils import timezone
from django.urls import reverse
from django.db.models import Exists, OuterRef, Subquery
/nix/store/4928ai9dfpvbh79908sll2x71xj91p9q-python3.11-projectify-0.1.0-static
```

To connect to the local postgres, you have to run the container using
`--network=host`. Set the correct `DATABASE_URL`, the below is only an example.
This also assumes, you have already created a database called `projectify`.
(use something like `createdb projectify`)

Try running seeddb:

```fish
podman run \
  --env-file backend/.env.production-sample \
  --env DATABASE_URL=postgres://$USER@localhost/projectify \
  --interactive \
  --network=host \
  projectify-manage:latest seeddb
```

This will start a server:

```fish
podman run \
  --env-file backend/.env.production-sample \
  --env DATABASE_URL=postgres://$USER@localhost/projectify \
  --interactive \
  --network=host \
  projectify-backend:latest
```

## Podman-compose

A sample `docker-compose.yml` file has been placed in `containers/`. Using
nixpkgs, you can run podman-compose with

```bash
nix run nixpkgs#podman-compose
```

Build and launch everything using

```bash
nix run nixpkgs#podman-compose -- \
  --file docker-compose.yaml \
  build
nix run nixpkgs#podman-compose -- \
  --file docker-compose.yaml \
  up
```

Create a new user

```bash
nix run nixpkgs#podman-compose -- \
  --file docker-compose.yaml \
  run migrate_backend createsuperuser
```

Connect to the Projectify app using the reverse proxy url at localhost:5000
