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

Integrating allauth adds the following URLs:

```
# allauth.socialaccount.views.ConnectionsView
# socialaccount_connections
/user/auth/
# allauth.socialaccount.providers.oauth2.views.view
# github_login
/user/auth/github/login/
# allauth.socialaccount.providers.oauth2.views.view
# github_callback
/user/auth/github/login/callback/
# allauth.socialaccount.views.LoginCancelledView
# socialaccount_login_cancelled
/user/auth/login/cancelled/
#allauth.socialaccount.views.LoginErrorView
# socialaccount_login_error
/user/auth/login/error/
# allauth.socialaccount.views.SignupView
# socialaccount_signup
/user/auth/signup/
```

Here's what these views do:

- `/user/auth`: Let user manage their *social account* connections. For
  example, they can link their account to GitHub, or remove an existing GitHub
  account connection
- `/user/auth/github/login`: Log in with GitHub
- `/user/auth/github/login/callback/`: GitHub redirects to this URL.
- `/user/auth/login/cancelled/`: Shows a "cancelled" error message when
  connecting the user cancels connecting their *social account*.
- `/user/auth/login/error/`: Shows an "error" error message when connecting
  a *social account* fails.
- `/user/auth/signup/`: Redirect to `/user/log-in`. We don't link this view.
Indirectly accessible when signing up a *social account*.

## Edit GitHub OAuth settings

1. Go to organization profile on GitHub
2. Open **Settings**.
3. Select **Developer settings** from the left menu
4. Open **OAuth Apps**
5. Press **Edit** next to the **Projectify** entry.

Things you can configure here:

- Create **Client secrets**: Note the `client_id` and `secret` here, and use
  them as `ALLAUTH_GITHUB_{CLIENT_ID,SECRET}` environment variables when
  starting the server.
- **Homepage URL**: Set this to `https://www.projectifyapp.com`
- **Authorization callback URL**: Set this to `https://www.projectifyapp.com/user/auth/github/login/callback/`


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
