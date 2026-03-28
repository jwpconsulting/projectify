<!--
SPDX-FileCopyrightText: 2024, 2026 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

This document contains coding conventions and snippets that you can copy
into your code while you work on the Projectify repository.

# Licensing

Add a copyright header to files if it's not there already.

Format for Python:

```python
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: YEAR RIGHT_HOLDER
```

Format for Django templates:

```jinja
{# SPDX-License-Identifier: AGPL-3.0-or-later #}
{# SPDX-FileCopyrightText: YEAR RIGHT_HOLDER #}
```

# Python

## Type annotations

- Try to annotate as many types as possible
- Prefer concrete types over `Any`.
- `Any` is an acceptable escape hatch when you can't find a concrete type.
- Annotate `type: ignore[override]` for when you override the type signature
of a parent class.
- Prefer `Union[a, b]` over `a | b`.
  This project will switch to the newer `a | b` syntax at some
  point, but it's good to keep it consistent for now.

# Imports

Prefer relative imports within an app. Here's an example from
`projectify/user/views/auth.py`:

```python
# Inside projectify/user/views/auth.py
# Good:
from ...services.internal import Token
# Bad:
from projectify.user.services.internal import Token
```

# Django

Projectify uses Django.

## Translation

In templates, mark all strings for translation with either `{% translate %}`
or `{% blocktranslate %}`. Examples:

```jinja2
<!-- from templates/workspace/workspace_settings_team_member_update.html -->
{% translate "Update team member" %}
{% blocktrans with workspace_title=workspace.title team_member=team_member %}Update {{ team_member }} in {{ workspace_title }} - Projectify{% endblocktrans %}
```

In Python files, use `django.utils.translation.gettext_lazy` like so:

```python
from django.utils.translation import gettext_lazy as _

_("Translate me")
```

When raising exceptions in Python code, use the following pattern:

```python
from django.utils.translation import gettext_lazy as _
raise Exception(_("Woah, weird value: {value}").format(value=1))
```


## Authentication

To annotate variables with user instances, prefer annotating the
concrete type `projectify/user/models.py:User`. Example:

```python
user: User = request.user
```

## Models

- All models should inherit from `projectify/lib/models.py:BaseModel`
- Prefer thin models over fat models.
- Put functions that interact with models in a corresponding services.

Example:

```python
# projectify/user/models.py
class UserInvite(BaseModel):
    """User invite model."""

    email = models.EmailField()
    user = models.ForeignKey[User](settings.AUTH_USER_MODEL)
    redeemed = models.BooleanField()

# projectify/user/services/user_invite.py
@transaction.atomic
def user_invite_create(*, email: str) -> Optional[UserInvite]:
    """Invite a user by email address."""
    user = user_find_by_email(email=email)
    if user:
        return None
    # TODO make this a selector
    invite_qs = UserInvite.objects.filter(redeemed=False, email=email)
    if invite_qs.exists():
        return invite_qs.get()
    return UserInvite.objects.create(email=email)
```

## Model admins

- Create a ModelAdmin for models.
- Try to give as few permissions as possible.
- The Django admin site is helpful for troubleshooting. For internal models,
it should only be used for troubleshooting.

Here's an example for a model that exposes internal state and shouldn't
be modified from the admin panel.

```python
# projectify/user/admin.py
@admin.register(UserInvite)
class UserInviteAdmin(admin.ModelAdmin[UserInvite]):
    """User invite admin."""

    list_filter = ("redeemed",)
    list_display = ("email", "redeemed")
    # Add fields that would make the app state inconsistent
    readonly_fields = ("user",)
```

## Services

Projectify models its service layer based on the
[Django Styleguide](https://github.com/HackSoftware/Django-Styleguide).

Services for the `Example` model are located in `app_name/services/example.py`.

Use `validate_perm` to check if a user can use a service function.
Here's an example for the `Task` model from the workspace app. The
caller of this service function passes `who: User` as a named parameter.

```python
validate_perm("workspace.create_task", who, section.project.workspace)
```

### Services transact and save

A service method MUST save all changes to the DB, and MUST handle its own
transaction, if an atomic transaction is needed.

### Permissions

Django calls an authorization a permission instead.
The method to see if a user has permission to perform an action is
called `has_perm` (if PermissionsMixin is subclasses).

A service layer function MUST check authorization. This allows to keep it
authorization logc in one location. A service layer function MUST perform
authorization with a given `who: User` argument. The `User` class MUST be
importedd from `user/models.py`.

Drawback: This couples our service layer tightly to the User model. When
testing service functions, you must create team members with the correct roles.

## Selectors

Selectors return querysets, lists of model instances or singular Optional model
instances.

Selectors for the `Example` model are located in
`app_name/selectors/example.py`.

In the case of a queryset or list return, name the selector the following:

```
<resource_name>_find_by_<most significant filter criterion>
```

For example, to define a function that find all `Example` instances
in a workspace choose the following name:

```
example_find_by_workspace
```

The reason to name it find, and not filter, is that filter implies ORM
chainability. Selectors should generally not be chained.

## Views

- Prefer function-based views over class based views.
- Django views must return HTTP status `400` for validation errors.

## Templates

- The app uses Django templates (not Jinja2).
- The app uses HTMX and only sometimes alpine.js
- Refer to `docs/templatetags.md` for guidance what template tags to use.

# Testing

Projectify uses pytest.

To test a specific test file with pytest, run the following:

```bash
uv run pytest $THE_FILE_YOU_WANT_TEST
```

## Test syntax

- Check what fixtures are available in `conftest.py` when you're writing tests.
- Use `pytestmark = pytest.mark.django_db` for tests that touch the database.

When you're testing a function `make_thing_bla`, write test class like this:

```python
class TestMakeThingBla:
    """Test make_thing_bla."""
```

When you're testing a class `ThingMaker`, write the test class like this:

```python
class TestThingMaker:
    """Test ThingMaker."""
```

For short functions or classes, prefer test functions. Here's an example
for `make_things_bla`:

```python
def test_make_things_bla(fixture_1: Fixture) -> None: ...
```

# Service layer
