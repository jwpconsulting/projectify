# Rate limiting implementation:

We use [Django Ratelimit, since the documentation specifically  mentions security](https://django-ratelimit.readthedocs.io/en/stable/security.html) to implement rate limiting. Requests we want to rate limit are:

- Requests that send emails as a consequence
- Log in / sign up requests

Another candidate was DRF's
[UserRateThrottle](https://www.django-rest-framework.org/api-guide/throttling/#userratethrottle).
Django Rest Framework invites developers to rate limit the views, but less for
security reasons. Django Rest Framework's Throttling documentation mentions
that it is not to be used as a security measure or DDoS protection.

It might also make sense to throttle services directly, not views. Any view
that is usable even when not authenticated is suited to be throttled directly.
Perhaps some services that are only usable when authenticated might be
throttable themselves. For now, we will keep throttling to views only.

# TODO

- [ ] Handle properly in frontend based on 429 status for ChangePassword,
  RequestEmailAddressUpdate and InviteUserToWorkspace

# Views to be rate limited

Views to be rate limited in the __user__ app:

- `RequestEmailAddressUpdate`, it sends an email with a confirm link
- `SignUp`, it sends an email with a confirm link
- `ChangePassword`, it informs users via email about the password change
- `PasswordResetRequest`, it sends a password reset link

Views to be rate limited in the __workspace__ app:

- `InviteUserToWorkspace`, sends an email to a user if they haven't created an
  account yet

# Rate limit settings

There are three types of rate limiting:

- using the user id (per user) as rate limiting key,
- using the request IP for not logged in users as rate limiting key, and
- using the contents of the request as a rate limiting key.

These three types can appear together by stacking django-ratelimit decorators.

- `SignUp` and `PasswordResetRequest` are used as an anonymous user, therefore
  we rate limit _per IP_. We want to rate limit based on the email address
  specified in the request as well.
- `ChangePassword`, `RequestEmailAddressUpdate`, and `InviteUserToWorkspace`
  are only usable when authenticated, therefore we rate limit _per user_.

Rate limits should be:

- `SignUp`, 5 times per hour _per IP_, 1 time per minute _per IP_
- `PasswordResetRequest`, 5 times per hour _per IP_, 5 times per hour _per
  request email_, 1 time per minute _per IP_
- `RequestEmailAddressUpdate`, 5 times per hour _per user_
- `ChangePassword`, 5 times per hour _per user_
- `InviteUserToWorkspace`, 10 times per hour _per user_

# How to rate limit services instead (idea)

If we want to enforce n times per email address per hour for auth services, we
can rate limit inside the service code instead.

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
