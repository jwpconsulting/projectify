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

## Dictionaries

Prefer updating values in dictionaries by replacing the whole dictionary.
Example:

```python
# Avoid
d = {"a": 1, "b": 2}
d["b"] = 3
d["new_value"] = 4
# Bettter
d = {"a": 1, "b": 2}
d = {**d, "b": 3, "new_value": 4}
```

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

# JavaScript

This project uses vanilla scripts in some templates. This project also
relies on HTMX.

Style conventions for writing JavaScript:

- Write strings with `"` quotes instead of `'`.
- Use four spaces of indentation (see `.editorconfig`, too)
- Try to return early in functions.

Prefer template strings. Example:

```javascript
// Avoid
'task-' + taskUuid + '-menu'
// Better
`task-${taskUuid}-menu`
```

When you're looking for elements inside the DOM with `getElementById`
and this element is *definitely* supposed to be there, throw an error.
Example:

```javascript
// BAD
table = section.querySelector("table");
// There'll be no useful output for developers when the table is missing
if (table) {
  doThingWithTable(table);
}
// GOOD
table = section.querySelector("table");
if (table === undefined) {
    throw new Error("Couldn't find table within this section");
}
doThingWithTable(table);
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

## URLs

Write named URLs like so:

```
workspace:workspaces:create-project
^         ^          ^     ^
|         |          |     hyphen
app name  |          |
          Workspace model
                     |
                     |
                     action
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
- Put the model `Model` for app `APP_NAME` in
  `projectify/APP_NAME/models.py:Model`


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

## Forms

- If a form field is required, don't specify `required=True`. Form fields
are `required=True` by default.

### Platform view

Use the `platform_view` decorator from `projectify/lib/views.py` for
view functions that require users to log in. Example:

```python
@platform_view
def log_in_first(request: AuthenticatedHttpRequest) -> HttpResponse: ...
```

## Templates

- The app uses Django templates (not Jinja2).
- The app uses HTMX, see `docs/frontend-scripting.md` for more.
- You can't use unsafe inline JavaScript or CSS. Use a `<script>` tag intead.
- You can't use HTMX's `hx-on` because that requires inline unsafe JavaScript.
- You can't use HTML `onclick` and similar event properties because that
  requires unsafe inline JavaScript.
- Refer to the **Template tags** section for guidance on what template tags to use.
- To style templates, Projectify uses [Tailwind version 3](https://v3.tailwindcss.com/). Refer to the tailwind
configuration at `tailwind.config.js`.

## Template includes

### Submit button

Here's the standard submit button for Projectify:

```jinja
{% load i18n %}
{% include "projectify/forms/submit.html" with text=_("Submit form") %}
{# Custom form name and value #}
{% include "projectify/forms/submit.html" with name="action" value="update" text=_("Update task") %}
{# Bind to different form #}
{% include "projectify/forms/submit.html" with form_name="other-form-name" text=_("Update task") %}
```

Parameters:

- `name`: Form name
- `value`: Value to submit
- `form_name`: Specify HTML form to bind to
- `text`: Show this text inside the button

## Template tags

This is a guide for using the template tags in the Projectify Django app.

### Permissions

Use the `has_perm` template tags from django rules like so:

```jinja
{% load rules %}
{% has_perm "workspace.create_team_member" user workspace as can_create_team_member %}
{% if can_create_team_member %}
  ...
{% endif %}
```

Here's how the project settings menu makes the project update link read-only:

```jinja
{# projectify/workspace/templates/workspace/workspace_settings_projects.html #}
{% has_perm "workspace.update_project" user workspace as can_update_project %}
{% if can_update_project %}
    <a href="{% url 'dashboard:projects:update' project_uuid=project.uuid %}"
       class="flex items-center gap-1 text-primary truncate">
        <span class="truncate">{{ project }}</span>
        <div class="w-4 h-4 shrink-0">{% icon "pencil" %}</div>
    </a>
{% else %}
    <span class="truncate">{{ project }}</span>
{% endif %}
```

See `projectify/rules.py` for all rules.

### Custom template tags

You can find the source code for the template tags in
`projectify/templatetags/projectify.py`

#### Percent

Formats a value as a percentage. Example:

```jinja
{% load projectify %}
{% percentage 100 %}
```

Renders to

```html
TODO
```

#### Anchor

Create an anchor with Tailwind styling. Usage:

```html
{% load projectify %}
{% anchor href="/" label=_("Learn more") external=True %}
```

This renders to the following. The styling is subject to change.

```html
<!-- TODO update -->
<a href="/"
   class="text-primary underline hover:text-primary-hover active:text-primary-pressed text-base"
   target="_blank"
  >Learn more<
  span class="sr-only">(Opens in new tab)</span>
  <svg ...></svg>
</a>
```

You can also remove `external=True`, or instead set `external=False`:

```jinja2
{% load projectify %}
{% anchor href="/" label=_("Learn more") %}
```

This renders to the following:

```html
<!-- TODO update -->
<a href="/"
   class="text-primary underline hover:text-primary-hover active:text-primary-pressed text-base"
   target="_blank"
  >Learn more</a>
```

You can also use the `anchor` template tag with a view name like so:

```jinja
{% load projectify %}
{% anchor href='dashboard:projects:update' label=_("Update") project_uuid=project.uuid %}
```

#### Circle button

Render a circular form `<button>`.

Example:

```jinja2
{% load projectify %}
{% circle_button TODO %}
```

#### Circle anchor

Render a circular icon with an anchor tag.

Available sizes:

- `4`
- `6`

Example:

```jinja2
{% load projectify %}
{% circle_anchor TODO %}
```

#### Action button

Render a form action button. Available colors:

- `secondary`
- `destructive`

Example:

```jinja2
{% load projectify %}
{% circle_anchor TODO %}
```

#### Go to action

Render a call to action anchor tag. Available colors:

- `primary`
- `secondary`
- `destructive`

Example:

```jinja2
{% load projectify %}
TODO
```

#### Icon

Render a heroicon. Available colors:

- `primary`
- `secondary`
- `destructive`

Sizes:

- `4`
- `6`

Example:

```jinja2
TODO
```

#### User avatar

Render a user avatar using the `user_avatar` template tag:

```jinja
{% load projectify %}
{% user_avatar user %}
```

If the user has a picture set, it renders to the following:

```html
<!-- TODO update -->
<div class="..."><img src="..." alt="user's preferred name"></div>
```

If there's not picture, it renders the following:

```html
<!-- TODO update -->
<div class="shrink-0 flex flex-row h-6 w-6 items-center rounded-full border border-primary bg-background"></div>
```

#### Picture

Render a `<picture>` tag with an image from static files:

```jinja
{% load projectify %}
{% picture src="image-of-cute-cats.png" alt="Cute cats" klass="w-8" %}
```

This renders to:

```html
<picture>
<img src="image-of-cute-cats.png" alt="Cute cats" width="180" height="180"
    class="w-8">
</picture>
```

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
