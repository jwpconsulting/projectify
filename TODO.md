# Bug

## Permissions (2023-10-20)

No permission checking is done beyond testing whether a user has access to a
resource based on whether they belong to a workspace or not. Especially roles
are not correctly considered at this point.

Some of the missing authorization (as of 2023-11-27)

- Task update
- Any read

# Typing

- Maybe: Type AbstractBaseUser to be the django.contrib.auth.models User
  instead

# Refactoring

- Remove all factories. They make tests slow, and we don't really need
so much extra things. Creating instances in conftests should be enough.
For more complicated things, we can write some `create_*` functions
in a /factory.py file for each app.
