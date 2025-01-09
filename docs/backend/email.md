---
title: Email testing snippets
date: 2025-01-05
author: Justus Perlwitz
---

<!--
SPDX-FileCopyrightText: 2025 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# How to test email delivery

To test sending an email from Render.com, you need to find the correct SSH
connection string. Please review [this document](https://render.com/docs/ssh)
to find out how to get the correct SSH connection string for your instance.

This is how it may look like:

```bash
ssh XXX@ssh.YYY.render.com
```

Open a Django shell using the following command in the ssh session you have
just connected to:

```bash
projectify-manage
```

Then, once the Django shell is open, you need to find a User model to send
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
