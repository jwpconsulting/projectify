<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Reverse proxy config

A reverse proxy passes requests from the user agent to the SSR frontend and the
Django backend.

Build the (Caddy based) reverse proxy like so:

<!-- TODO update the following instructions -->

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
