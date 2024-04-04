# Password validation

## Backend

There are two points in the user facing services where we allow setting a password:

- `user_sign_up` in `user/services/auth.py`
- `user_change_password` in `user/services/user.py`, and

These services are accessible through the following URLs:

- `user/user/sign-up`
- `user/user/change-password`, and

We should use `validate_password` from
`django.contrib.auth.password_validation`, [documentation here](https://docs.djangoproject.com/en/5.0/topics/auth/passwords/#django.contrib.auth.password_validation.validate_password)
in both services. Here we should ensure that the ValidationError gets attached
to the correct serializer field, so that a clean JSON error object will come
back to our client.

Furthermore, we should expose the password validators to our frontend using a
new API, which should be usable without having to log in, such as

`user/user/password-validators` GET

which returns a list of _help texts_, as [documented here](https://docs.djangoproject.com/en/5.0/topics/auth/passwords/#django.contrib.auth.password_validation.password_validators_help_texts).

## Frontend

The two APIs above are accessed from the following routes:

- `user/sign-up`
- `user/profile/change-password`

While `src/lib/repository/user.ts` contains the repository functions that
return validation errors in case of an error.

If a password can not be validated, errors should come back with HTTP status
400. Then, we should render the password validation errors inline.
