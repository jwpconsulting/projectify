# Podman / Docker

This assumes that you are using [Podman](https://podman.io/). The five
commands contained in their respective containers

- projectify-backend (contains projectify-manage as well)
- projectify-celery
- projectify-frontend
- projectify-revproxy

can be built from the repository's root directory using the Nix `flake.nix`
packages and copied into the local container storage like so:

```bash
# Podman 4.3.1 struggles loading gzipped docker containers, so we do this
# instead:
bash $(nix build --print-out-paths --no-link .#projectify-backend-container) | podman load
bash $(nix build --print-out-paths --no-link .#projectify-frontend-node-container) | podman load
bash $(nix build --print-out-paths --no-link .#projectify-celery-container) | podman load
bash $(nix build --print-out-paths --no-link .#projectify-revproxy-container) | podman load
```

Try running projectify-manage using

```bash
podman run \
  --env-file backend/.env.production-sample \
  projectify-backend:latest \
  projectify-manage shell -c 'from django.conf import settings; print(settings.STATIC_ROOT)'
```

This prints something like the following

```
[...]
from django.utils import timezone
from django.urls import reverse
from django.db.models import Exists, OuterRef, Subquery
/nix/store/4928ai9dfpvbh79908sll2x71xj91p9q-python3.11-projectify-0.1.0-static
```

## Podman-compose

A sample `docker-compose.yml` file has been placed in the root folder. This
assumes that you are in a Nix flake shell in the root directory or use
nix-direnv. After you have build and loaded the above images, you can launch
everything using

```bash
podman-compose up
```

Create a new user from the shell

```bash
podman-compose run migrate_backend projectify-manage shell -c 'from projectify.user.services import internal; internal.user_create_superuser(email="admin@localhost", password="password")'
```

Connect to the Projectify app using the reverse proxy url at localhost:5000
