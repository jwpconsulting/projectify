# Throttling implementation

We might want to [UserRateThrottle](https://www.django-rest-framework.org/api-guide/throttling/#userratethrottle) to make sure some requests aren't sent too often. Requests we want to throttle are:

- Requests that send emails as a consequence
- Log in / sign up requests

Django Rest Framework invites developers to rate limit the views, but I wonder
if it also makes sense to throttle services themselves.

Any view that is usable even when not authenticated is suited to be throttled
directly. Perhaps some services that are only usable when authenticated might
be throttable themselves. For now, we will keep throttling to views only.

Django Rest Framework's Throttling documentation mentions that it is not to be
used as a security measure or DDoS protection.

An alternative could be [Django Ratelimit, since the documentation specifically  mentions security](https://django-ratelimit.readthedocs.io/en/stable/security.html)

# Views to be throttled

Throttlabe views in __user__ app:

- `RequestEmailAddressUpdate`, it sends an email with a confirm link
- `SignUp`, it sends an email with a confirm link
- `ChangePassword`, it informs users via email about the password change
- `PasswordResetRequest`, it sends a password reset link

Throttlable views in __workspace__:

- `InviteUserToWorkspace`, sends an email to a user if they haven't created an
  account yet

# DRF throttle classes

If we end up using DRF Throttling, the Throttle classes we would want to use
are:

- `SignUp` and `PasswordResetRequest` are used as an anonymous user, therefore
  we use `AnonRateThrottle`. We want to throttle based on the email address
  used as well.
- `ChangePassword`, `RequestEmailAddressUpdate`, and `InviteUserToWorkspace`
  are only usable when authenticated, therefore we use `UserRateThrottle`.

Throttle amounts should be:

`AnonRateThrottle`, 60 requests per IP per hour, 1 request per email per 10
minutes
`UserRateThrottle`, 60 requests per user per hour

# How to throttle services instead

If we want to enforce n times per email address per hour for auth services, we
can put the throttling inside the service code instead.

For example, `user_sign_up`, could be something like this:

```python
def user_sign_up(
  *,
  email: str,
  password: str,
  tos_agreed: bool,
  privacy_policy_agreed: bool,
) -> User:
    """Sign up a user."""
  validate_rate(key=email, rate='60/d')
  # Check if user exists
  if user_find_by_email(email=email) is not None:
    pass
  # ... Rest
```

Where `validate_rate` throws a `exceptions.Throttled` DRF exception.
