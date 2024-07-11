# Reverse proxy config

A reverse proxy passes requests from the user agent to the SSR frontend and the
Django backend.

Build the (Caddy based) reverse proxy like so:

```bash
podman build --target projectify-revproxy -t projectify-revproxy:latest -f projectify-revproxy.Dockerfile .
```

Launch the reverse proxy:

```bash
podman run \
  --interactive \
  --network=host \
  projectify-revproxy:latest
```
