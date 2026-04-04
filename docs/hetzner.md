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

- `/usr/share/projectify/release/current/static`: Projectify static files
- `/usr/share/projectify/releases/current/venv`: Python virtual environmeny
- `/usr/share/projectify/releases/current/app`: Projectify repository (no git clone)
- `/var/lib/projectify`: `projectify` user home directory
- `/var/lib/projectify/state`: `projectify` user application state (but not
  PostgreSQL)
- `/var/lib/projectify/state/media`: User uploaded media
- `/var/gunicorn.socket`: Gunicorn socket, owner is `projectify:projectify`

## Backups

- Rsync media backup runs hourly
- pgBackRest backup runs a full backup daily, and a differential backup hourly

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

# Migration procedure

1. Take Render.com instance down / maintenance mode
2. Create database backup with pg_dump
3. Upload database backup to new Hetzner instance
4. Restore database backup with pg_restore
5. Update DNS record to point at `www.projectifyapp`.

## Upload database backup

```bash
rsync \
    -e 'ssh -i KEY -o ProxyCommand="ssh -i KEY -W %h:%p root@PUBLIC_IP"' \
    ARCHIVE.dir.tar.gz \
    root@10.0.0.3:/var/lib/projectify/
```

## Restore database backup

Reference: <https://render.com/docs/postgresql-backups#restoring-from-a-backup-file>

```bash
cd /var/lib/projectify/db_dumps
tar -zxvf 2026-04-04T08_14Z.dir.tar.gz
# List contents
ls -la
ls 2026-04-04T08:14Z
```

Output:

```
./
./2026-04-04T08:14Z/
./2026-04-04T08:14Z/projectify_postgres_production/
./2026-04-04T08:14Z/projectify_postgres_production/…
…
total 268
drwxr-sr-x 3       1000       1000   4096 Apr  4 08:15 .
drwx------ 9 projectify projectify   4096 Apr  4 08:19 ..
drwxr-sr-x 3       1000       1000   4096 Apr  4 08:15 2026-04-04T08:14Z
-rw-r--r-- 1 root       root       256500 Apr  4 08:17 2026-04-04T08_14Z.dir.tar.gz

drwxr-sr-x 3 1000 1000 4096 Apr  4 08:15 .
drwxr-sr-x 3 1000 1000 4096 Apr  4 08:15 ..
drwx--S--- 2 1000 1000 4096 Apr  4 08:15 projectify_postgres_production
```

Restore:

```bash
sudo chown postgres:postgres 2026-04-04T08:14Z/projectify_postgres_production
sudo -u postgres pg_restore \
    --dbname=projectify \
    --verbose \
    --clean \
    --if-exists --no-owner --no-privileges \
    --format=directory \
    2026-04-04T08:14Z/projectify_postgres_production
```

Output:

```
pg_restore: connecting to database for restore
…
pg_restore: creating FK CONSTRAINT "public.workspace_teammember workspace_workspaceuser_user_id_…_fk_user_user_id"
```

Check schema:

```
sudo -u projectify psql -c "\d"
```

Output:

```
                            List of relations
 Schema |                   Name                    |   Type   |  Owner
--------+-------------------------------------------+----------+----------
 public | account_emailaddress                      | table    | postgres
 public | account_emailaddress_id_seq               | sequence | postgres
 public | account_emailconfirmation                 | table    | postgres
 public | account_emailconfirmation_id_seq          | sequence | postgres
 public | auth_group                                | table    | postgres
 public | auth_group_id_seq                         | sequence | postgres
 public | auth_group_permissions                    | table    | postgres
 public | auth_group_permissions_id_seq             | sequence | postgres
 public | auth_permission                           | table    | postgres
 public | auth_permission_id_seq                    | sequence | postgres
 public | blog_post                                 | table    | postgres
 public | blog_post_id_seq                          | sequence | postgres
 public | blog_postcontent                          | table    | postgres
 public | blog_postcontent_id_seq                   | sequence | postgres
 public | corporate_coupon                          | table    | postgres
 public | corporate_coupon_id_seq                   | sequence | postgres
 public | corporate_customer                        | table    | postgres
 public | corporate_customer_id_seq                 | sequence | postgres
 public | django_admin_log                          | table    | postgres
 public | django_admin_log_id_seq                   | sequence | postgres
 public | django_celery_results_chordcounter        | table    | postgres
 public | django_celery_results_chordcounter_id_seq | sequence | postgres
 public | django_celery_results_groupresult         | table    | postgres
 public | django_celery_results_groupresult_id_seq  | sequence | postgres
 public | django_celery_results_taskresult          | table    | postgres
 public | django_celery_results_taskresult_id_seq   | sequence | postgres
 public | django_content_type                       | table    | postgres
 public | django_content_type_id_seq                | sequence | postgres
 public | django_migrations                         | table    | postgres
 public | django_migrations_id_seq                  | sequence | postgres
 public | django_session                            | table    | postgres
 public | pg_stat_statements                        | view     | postgres
 public | pg_stat_statements_info                   | view     | postgres
 public | socialaccount_socialaccount               | table    | postgres
 public | socialaccount_socialaccount_id_seq        | sequence | postgres
 public | socialaccount_socialapp                   | table    | postgres
 public | socialaccount_socialapp_id_seq            | sequence | postgres
 public | socialaccount_socialtoken                 | table    | postgres
 public | socialaccount_socialtoken_id_seq          | sequence | postgres
 public | user_previousemailaddress                 | table    | postgres
 public | user_previousemailaddress_id_seq          | sequence | postgres
 public | user_user                                 | table    | postgres
 public | user_user_groups                          | table    | postgres
 public | user_user_groups_id_seq                   | sequence | postgres
 public | user_user_id_seq                          | sequence | postgres
 public | user_user_user_permissions                | table    | postgres
 public | user_user_user_permissions_id_seq         | sequence | postgres
 public | user_userinvite                           | table    | postgres
 public | user_userinvite_id_seq                    | sequence | postgres
 public | workspace_chatmessage                     | table    | postgres
 public | workspace_chatmessage_id_seq              | sequence | postgres
 public | workspace_label                           | table    | postgres
 public | workspace_label_id_seq                    | sequence | postgres
 public | workspace_project                         | table    | postgres
 public | workspace_section                         | table    | postgres
 public | workspace_section_minimized_by            | table    | postgres
 public | workspace_section_minimized_by_id_seq     | sequence | postgres
 public | workspace_subtask                         | table    | postgres
 public | workspace_subtask_id_seq                  | sequence | postgres
 public | workspace_task                            | table    | postgres
 public | workspace_task_id_seq                     | sequence | postgres
 public | workspace_tasklabel                       | table    | postgres
 public | workspace_tasklabel_id_seq                | sequence | postgres
 public | workspace_teammember                      | table    | postgres
 public | workspace_teammemberinvite                | table    | postgres
 public | workspace_workspace                       | table    | postgres
 public | workspace_workspace_id_seq                | sequence | postgres
 public | workspace_workspaceboard_id_seq           | sequence | postgres
 public | workspace_workspaceboardsection_id_seq    | sequence | postgres
 public | workspace_workspaceuser_id_seq            | sequence | postgres
 public | workspace_workspaceuserinvite_id_seq      | sequence | postgres
(71 rows)
```

# Implement rolling releases

Directory structure:

- `/usr/share/projectify/releases`
- `/usr/share/projectify/releases/{DATE_GIT_COMMIT_SHA}`
- `/usr/share/projectify/releases/{DATE_GIT_COMMIT_SHA}/venv`: Python virtualenv
- `/usr/share/projectify/releases/{DATE_GIT_COMMIT_SHA}/app`: Projectify source code
- `/usr/share/projectify/releases/{DATE_GIT_COMMIT_SHA}/static`: Projectify static files

Symbolic links:

- `/usr/share/projectify/releases/current` to
  `/usr/share/projectify/releases/{DATE_GIT_COMMIT_SHA}`
- `/var/lib/projectify/venv` to `/usr/share/projectify/releases/current/venv`
- `/var/lib/projectify/app` to `/usr/share/projectify/releases/current/app`
- `/usr/share/projectify/static` to `/usr/share/projectify/releases/current/static`

# Monitoring

Connect to Bastio

ssh root@204.168.222.148 -i ~/.ssh/id_rsa_yubikey.pub -L 3000:localhost:3000

Create Grafana user on SSH bastion:

```bash
read PASSWORD
grafana-cli admin reset-admin-password $PASSWORD
```

Strong password policy documentation: <https://grafana.com/docs/grafana/next/setup-grafana/configure-access/configure-authentication/grafana/#strong-password-policy>

# To Do

Investigate what this means:

```
projectify-bastion dhcpcd[971]: ps_root_recvmsg: Operation not permitted
```

- Find a good way to integrate Gunicorn with Prometheus/Grafana
- Find a good way to integrate Django with Prometheus/Grafana
- Find a good way to integrate Caddy with Prometheus/Grafana
- Add Grafana alerting
- Remove whitenoise, use serve-static on projectify-demo

# Done

- Implement rolling releases
