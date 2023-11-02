# Bug

## Authorization (2023-10-20)

No authorization check is done beyond testing whether a user has access to a
resource based on whether they belong to a workspace or not. Especially roles
are not correctly considered at this point.

# Typing

- Maybe: Type AbstractBaseUser to be the django.contrib.auth.models User
  instead
