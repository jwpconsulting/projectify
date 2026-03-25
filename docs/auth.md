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

## Edit Google OAuth settings

Source: <https://docs.allauth.org/en/latest/socialaccount/providers/google.html>

1. Open the Google developers console
2. Go to **Credentials**
3. Press **Create project** and follow the instructions to create a project.
4. Press **Configure consent screen**. You should land on the **Branding** page
   with the text "Google Auth Platform not configured yet".
5. Press **Get started**.
6. Enter an app name and select an email contact.
7. Select **External** as the Audience.
8. Enter an email address under **Contact Information**.
9. Agree to the terms of service.
10. On the next **OAuth Overview** page, press **Create OAuth client**.
11. Select "Web application" as **Application type** and enter a OAuth 2.0
    client name.
12. Add the following redirect URI under **Authorized redirect URIs**:
  `https://www.projectifyapp.com/user/auth/google/login/callback/`
13. Press **Create**.

Copy the **Client ID** and **Client secret** from the **OAuth client created**
overlay. These are your
`ALLAUTH_GOOGLE_CLIENT_ID` and `ALLAUTH_GOOGLE_SECRET` environment variables.

Note: For local development, use the following redirect URI.

```
http://localhost:8000/user/auth/google/login/callback/
```

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

# Allauth bug

1. Create normal user account
2. Somehow connect with GH
3. Go to admin, delete `SocialAccount` record
4. Log out
5. Log in with GH
6. password is wiped

## Evidence

Here's code that might be responsible for the password being wiped

```python
# https://github.com/pennersr/django-allauth/blob/cf7f55d79e421e5d5ba078e31119a799f8b149e8/allauth/socialaccount/models.py#L397
# allauth/socialaccount/models.py#L397
def _accept_login(self, request) -> None:
        from allauth.socialaccount.internal.flows.email_authentication import (
            wipe_password,
        )

        if self._did_authenticate_by_email:
            wipe_password(request, self.user, self._did_authenticate_by_email)
            if app_settings.EMAIL_AUTHENTICATION_AUTO_CONNECT:
                self.connect(context.request, self.user)
```

`_login` calls `_accept_login` here:

```python
# https://github.com/pennersr/django-allauth/blob/cf7f55d79e421e5d5ba078e31119a799f8b149e8/allauth/socialaccount/internal/flows/login.py#L20
# allauth/socialaccount/internal/flows/login.py#L20
def _login(request, sociallogin):
    sociallogin._accept_login(request)
    record_authentication(request, sociallogin)
    return perform_login(
        request,
        sociallogin.user,
        email_verification=app_settings.EMAIL_VERIFICATION,
        redirect_url=sociallogin.get_redirect_url(request),
        signal_kwargs={"sociallogin": sociallogin},
    )
```

`_authenticate` in the same module calls `_login` here:

```python
# https://github.com/pennersr/django-allauth/blob/cf7f55d79e421e5d5ba078e31119a799f8b149e8/allauth/socialaccount/internal/flows/login.py#L72-L82
# allauth/socialaccount/internal/flows/login.py#L72
def _authenticate(request, sociallogin):
    if request.user.is_authenticated:
        get_account_adapter(request).logout(request)
    if sociallogin.is_existing:
        # Login existing user
        ret = _login(request, sociallogin)
    else:
        # New social user
        ret = process_signup(request, sociallogin)
    return ret
```

`complete_login` in same file calls `_authenticate`:

```python
def complete_login(request, sociallogin, raises=False):
    try:
        pre_social_login(request, sociallogin)
        process = sociallogin.state.get("process")
        if process == AuthProcess.REDIRECT:
            return _redirect(request, sociallogin)
        elif process == AuthProcess.CONNECT:
            if raises:
                do_connect(request, sociallogin)
            else:
                return connect(request, sociallogin)
        else:
            return _authenticate(request, sociallogin)
    except SignupClosedException:
        if raises:
            raise
        return render(
            request,
            f"account/signup_closed.{account_settings.TEMPLATE_EXTENSION}",
        )
    except ImmediateHttpResponse as e:
        if raises:
            raise
        return e.response
```

`complete_social_login` in `allauth/socialaccount/helpers.py` is a thin
wrapper for `complete_login`.

Finally, the `OAuthCallbackView` calss in
`allauth/socialaccount/providers/oauth/views.py` calls `complete_social_login`:

```python
# allauth/socialaccount/providers/oauth/views.py#L116
class OAuthCallbackView(OAuthView):
    def dispatch(self, request):
        """
        View to handle final steps of OAuth based authentication where the user
        gets redirected back to from the service provider
        """
        provider = self.adapter.get_provider()
        login_done_url = reverse(f"{self.adapter.provider_id}_callback")
        client = self.adapter._get_client(request, login_done_url)
        if not client.is_valid():
            if "denied" in request.GET:
                error = AuthError.CANCELLED
            else:
                error = AuthError.UNKNOWN
            return render_authentication_error(
                request,
                provider,
                error=error,
                extra_context={
                    "oauth_client": client,
                    "callback_view": self,
                },
            )
        app = provider.app
        try:
            access_token = client.get_access_token()
            token = SocialToken(
                token=access_token["oauth_token"],
                # .get() -- e.g. Evernote does not feature a secret
                token_secret=access_token.get("oauth_token_secret", ""),
            )
            if app.pk:
                token.app = app
            login = self.adapter.complete_login(
                request, app, token, response=access_token
            )
            login.token = token
            login.state = SocialLogin.unstash_state(request)
            return complete_social_login(request, login)
        except OAuthError as e:
            return render_authentication_error(request, provider, exception=e)
```

Call chain (top-down)

1. `OAuthCallbackView.dispatch`
2. `complete_social_login`
3. `complete_login`
4. `_authenticate`
5. `_login`
6. `_accept_login`
7. `wipe_password`

## Config review

```python
# projectify/settings/base.py
    ACCOUNT_USER_MODEL_USERNAME_FIELD = None
    ACCOUNT_SIGNUP_FIELDS = [
        "email*",
        "password1*",
        "password2*",
        "tos_agreed*",
        "privacy_policy_agreed*",
    ]
    ACCOUNT_LOGIN_METHODS = {"email"}
    LOGIN_REDIRECT_URL = "/user/profile"
    ACCOUNT_SIGNUP_REDIRECT_URL = "/onboarding"
    ACCOUNT_EMAIL_VERIFICATION = "none"

    # django allauth social account settings
    # --------------------------
    SOCIALACCOUNT_ONLY = True
    SOCIALACCOUNT_AUTO_SIGNUP = False
    SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
    SOCIALACCOUNT_FORMS = {
        "signup": "projectify.user.forms.SocialAccountSignUpForm",
    }
```

The solution may be to disable `SOCIALACCOUNT_EMAIL_AUTHENTICATION`.
