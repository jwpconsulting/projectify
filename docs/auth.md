<!--
SPDX-FileCopyrightText: 2024,2026 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# User account management

User account models are stored in `projectify/user/models.py`.

## Foreign key to User

There's nothing wrong with coupling!

Implement a foreign key pointing at a user like so:

```python
from projectify.user.models import User

class MyModel(models.Model):
    user = models.ForeignKey["User"](User, on_delete=models.CASCADE)
```

## Testing

Prefer using `projectify.user.models.User` over Django's
`AbstractBaseUser` or `AbstractUser` in test cases and fixtures.

# django-allauth

Projectify uses django-allauth. django-allauth has many features. It doesn't
replace Projectify's existing authentication code.

- GitHub callback URL: `https://www.projectifyapp.com/user/github/login/callback/`

# Naming things in authentication

## Log In

The act of using user credentials to authenticate with Projectify and create a
session to be used for further authentication, e.g., when performing API
requests as a user.

The verb is

> I will _log in_ with my credentials

The adjective form is

> my _login_ information.

Theoretically, there could be a noun, such as

> my _login_

or

> proceed to the _login_

but we try to avoid saying that, since it sounds clunky and suggesting another
word will follow it, such as _login form_, at which stage it becomes an
adjective again. _log-in_ as the noun form also sounds awkward, so we avoid
that, too.

## Sign Up

The act of requesting a new user account to be created using the specified
credentials.

The verb is

> _Sign up_ here

The adjective form is

> Click here to proceed to the _signup_ form

We try to avoid using the noun form _signup_, but do not use _sign-up_, for the
same reason we do not use _log-in_.

## Log out

The act of removing an authenticated user session. The application server
instructs the browser to remove the session cookie from its cookie jar. The
application server purges the record of this authenticated sessionm from its
session storage.

Same as Log in. As a verb we can use it like

> I will _log out_ of my account

As an adjective, if we ever use it, it would be:

> a logout page

But most likely, since a log out is very past tense, we would say things like

> a logged out user

## Sign in

To keep our terminology uniform, we prefer log in over sign in.
