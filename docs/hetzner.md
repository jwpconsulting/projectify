---
title: Hetzner deployment
date: 2026-04-03
author: Justus Perlwitz
---
<!--
SPDX-FileCopyrightText: 2026 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

This document outlines the Hetzner deployment for Projectify hosted
on <https://www.projectifyapp.com>.

```
        | SSH traffic     .-------------------------------------.
        |                 | Projectify app server               |
        v         Jump    |                                     |
  .-------------. Proxy   +------.                              |
  | SSH Bastion |-----FW--> sshd |                              |
  .-------------.  Priv.  +------.                              |
        ^          netw.  |                                     |
        |                 |                                     |
        | SSH tunnel  .-----Prometheus                          |
        |             |   |                                     |
  .-------------.     |   | Static files   .----> PostgreSQL -------.
  | Monitoring  |<----.   |    ^           |                    |   |
  .-------------.  Priv.  |    |           |                    |   |
        |          netw.  |    |           |                    |   |
        | Alerting        |   Caddy --> gunicorn -> Media       |   | Hourly
        v                 |    ^  |                  ^  |       |   | pg_dump
  .---------.             |    |  |                  |  |       |   |
  | Mailgun |             |    |  .------------------.  |       |   |
  .---------.             |    |    sendfile(2)         |       |   |
                          |    |                        |       |   |
                          .--- | ---------------------+-|-------.   |
                               |  .---------------.   | |           |
   .---------. HTTPS           |  | Hetzner       |   | |           |
   | Browser |-----------------.  | daily backups |<--. |           |
   .---------.                    .---------------.     | Hourly    |
                                                        | rsync     |
                                           .------------. backup    |
                                           |                        |
                                           v                        |
                                         .-----------------------.  |
                                         | Hetzner block storage |<-.
                                         .-----------------------.
```

# SSH bastion

Forwards authenticated ssh connections to the Projectify app server.
Monitoring is integrated into the SSH bastion for simplicity

Hetzner configuration:

- `eth0`: Global address
- `enp7s0`: Private network, `10.0.0.2`
- Daily backups

Software:

- Debian 13
- OpenSSH
- Grafana dashboard

Firewall:

- Incoming:
  - Allow 22/tcp incoming
  - Deny all other incoming
- Outgoing:
  - Allow 22/tcp outgoing to private network
  - Deny all other outgoing to private network
  - Allow other outgoing

## Connect to Grafana

Connect to Grafana using SSH forwarding, like this:

```bash
ssh -L 80:localhost:80 -N user@BLA
```

# Projectify app server

Hetzner configuration

- VPS name: `projectify-app-server`
- Specs:
  - 2 vCPUs
  - 8 GB Ram
  - 80 GB Disk Local
  - 100 GBBlock storage `projectify-app-server-backup-storage` attached to
    `/dev/disk/by-id/scsi-0HC_Volume_XXXXXXXXX`, mounted to `/srv/backups`
- `eth0`: Global address
- `enp7s0`: Private network, `10.0.0.3`
- Daily backups

Runs the following software:

- Debian 13
- PostgreSQL
- Caddy
- Projectify Django app
- OpenSSH
- Prometheus exports metrics
- rsync: Hourly backup to block storage to `/srv/backups/projectify_app_media` on
  block storage
- pgBackRest: Hourly PostgreSQL backups to `/src/backups/pgbackrest` on block
  storage

Firewall:

- Allow 80,443/tcp incoming
- Allow 22/tcp from SSH bastion
- Deny all other incoming
- Allow other outgoing

Caddy configuration:

- Serve Projectify app static file requests directly
- Reverse proxy application requests to Projectify Django/gunicorn process
- Serve media files after receiving ticket from Django app

Django/gunicorn configuration:

- Serve Projectify
- django-sendfile[^sendfile] configured
- Serve app locally from `unix:/run/gunicorn.sock`
- Log to syslog

[^sendfile]: <https://django-sendfile2.readthedocs.io/en/latest/>

Create users:

- `projectify` user with `projectify` group, runs gunicorn
- Add `caddy` user to `projectify` group

Application data:

- `/usr/share/projectify/static`: Projectify static files
- `/var/lib/projectify`: `projectify` user home directory
- `/var/lib/projectify/venv`: Python virtual environmeny
- `/var/lib/projectify/app`: Projectify repository (no git clone)
- `/var/lib/projectify/state`: `projectify` user application state (but not
  PostgreSQL)
- `/var/lib/projectify/state/media`: User uploaded media
- `/var/gunicorn.socket`: Gunicorn socket, owner is `projectify:projectify`

Backup directories:

- `/srv/backups/pgbackrest`: pgBackRest stores database backups here
- `/srv/backups/projectify_app_media`: rsync stores Projectify user uploaded media files here

# System requirements

- Latency: The landing page shall be served within 600 ms (*load* metric),
  assuming "Regular 4G / LTE" throttling and "Disabled Cache" set in the
  Firefox developer console **Network** tab.
- Round-trip latency: The Projectify app server shall begin serving any
  incoming request within 500 ms, including TLS handshake and round trip
  latency for the first application data containing https packet. Verify
  with **Timings** tab in the **Network** tab in the Firefox developer console.
  Example for `GET https://www.projectifyapp.com/` with `HTTP/2`:
    - **Blocked**: 0 ms
    - **DNS Resolution**: 2 ms
    - **Connecting**: 5 ms
    - **TLS Setup**: 13 ms
    - **Sending**: 0 ms
    - **Waiting**: 179 ms
    - **Receiving**: 0 ms
- Access control: Only authorized system administrators shall have root access
  to the Projectify production environment, including the Projectify app
  server.
- SSH hardening: The Projectify production environment shall prevent
  unauthorized third parties from connecting to servers in the Projectify
  production environment. This includes probing or bruteforcing the OpenSSH
  server running on the Projectify app server
- Availability: The Projectify production environment shall serve user traffic
  with at least 99.9% monthly uptime
- Monitoring: The Projectictify production environment shall inform system
  administrators of any outages within 1 hour
- Integrity: The Projectify production environment shall contain technical
  measures to prevent data loss
- Recovery point objective: After an outage or data loss event, data dating back
to 1 hour before that event shall be recoverable.
- Recovery time objective: Any major outage involving data loss shall be
  resolved within one day.

# Organizational requirements

- Access control: Only authorized system administrators shall hold root
access credentials or other credentials to access internal management
interfaces
- Protected credentials: All access credentials shall be protected with strong
encryption and stored on tamper-proof hardware, such as smart cards.
- Reproducible deployment: All server configuration shall be reproducible using
  automation software such as Ansible.

# Ansible usage

## Inventory

Create inventory in `ansible/inventory.yml`:

```yaml
all:
  hosts:
    ssh_bastion:
      ansible_host: BASTION_HOSTNAME
      ansible_user: root
      ansible_ssh_extra_args: "-o ControlMaster=auto -o ControlPersist=60s"
      ansible_ssh_pipelining: true
    projectify_app:
      ansible_host: 10.0.0.3
      ansible_user: root
      ansible_ssh_common_args: '-o ProxyJump=BASTION_HOSTNAME'
      backup_storage_path '/dev/disk/by-id/scsi-0HC_Volume_XXX'
      ansible_ssh_extra_args: "-o ControlMaster=auto -o ControlPersist=60s"
      ansible_ssh_pipelining: true
```

If you use identity files, you may have to use ssh args like this:

```yaml
ansible_ssh_common_args: '-i $KEYFILE -o ProxyCommand="ssh -i $KEYFILE -W %h:%p root@BASTION_HOSTNAME"'
```

## SSH Bastion

Test if you can reach the SSH bastion:

```bash
ansible -i ansible/inventory.yml -m ping ssh_bastion
```

Expected output:

```
ssh_bastion | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

Configure SSH bastion with Ansible:

```bash
ansible-playbook -i ansible/inventory.yml -l ssh_bastion ansible/playbook.yml
```

## Application server

Test if you can reach the application server:

```bash
ansible -i ansible/inventory.yml -m ping projectify_app
```

Expected output:

Configure SSH bastion with Ansible:

```bash
ansible-playbook -i ansible/inventory.yml -l projectify_app ansible/playbook.yml
```
