---
title: Email deliverability tests
date: 2025-01-05
updated: 2026-06-01
author: Justus Perlwitz
---

<!--
SPDX-FileCopyrightText: 2025-2026 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# How to test email delivery

To test sending an email from Projectify on Hetzner, connect to the app server
through the SSH bastion. Open a Django shell using the following commands:

```bash
cd /usr/share/projectify/releases/current
sudo -u projectify \
  DJANGO_SETTINGS_MODULE=projectify.settings.hetzner \
  DJANGO_CONFIGURATION=Hetzner \
  STATIC_ROOT=$PWD/static \
  MEDIA_ROOT=/var/lib/projectify/state/media \
  DATABASE_URL=postgresql://projectify@localhost/projectify \
  CREDENTIALS_FILE=/var/lib/projectify/credentials.toml \
  venv/bin/python app/manage.py shell
```

In the Django shell, find a User to send
emails to. These are the two Python commands needed to import the User model
and find a User by email address.

```python
from projectify.user.models import User
u = User.objects.get(email="your@email.here")  # your email
```

For instance, when looking for the user with email address `email@example.com`,
this is how it may look like inside the Django shell:

```python
>>> from projectify.user.models import User
>>> u = User.objects.get(email="email@example.com")  # your email
>>> u
<User: ExampleUser>
>>> u.email
'email@example.com'
```

Then, you need to import an Email class and instantiate it with the user picked
before. Once the class is instantiated, you can run `.send()` on the instance.
This is how to achieve this in the Django shell:

```python
from projectify.user.emails import UserEmailConfirmationEmail
e = UserEmailConfirmationEmail(receiver=u, obj=u)
e.send()
```

A successful run of these three commands looks like this:

```python
>>> from projectify.user.emails import UserEmailConfirmationEmail
>>> e = UserEmailConfirmationEmail(receiver=u, obj=u)
>>> e.send()
```

# Test admin email

To test emailing admins, run the following commands in a Django shell:

```
from django.core.mail import mail_admins
mail_admins("Test subject", "Test message")
```

Review the current admins by inspecting the value of the `settings.ADMINS` variable. Here's an example:

```
>>> settings.ADMINS
[['Foo', 'foo+bar@example.com']]
```
