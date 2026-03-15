---
title: Backend template tags guide
---
<!--
SPDX-FileCopyrightText: 2025 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

This is a guide for using the template tags in the Projectify Django app.

# Permissions

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

# Custom template tags

You can find the source code for the template tags in
`projectify/templatetags/projectify.py`

## Percent

Formats a value as a percentage. Example:

```jinja
{% load projectify %}
{% percentage 100 %}
```

Renders to

```html
TODO
```

## Anchor

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

## circle button

Render a circular form `<button>`.

Example:

```jinja2
{% load projectify %}
{% circle_button TODO %}
```

## circle anchor

Render a circular icon with an anchor tag.

Available sizes:

- `4`
- `6`

Example:

```jinja2
{% load projectify %}
{% circle_anchor TODO %}
```

## action button

Render a form action button. Available colors:

- `secondary`
- `destructive`

Example:

```jinja2
{% load projectify %}
{% circle_anchor TODO %}
```

## go to action

Render a call to action anchor tag. Available colors:

- `primary`
- `secondary`
- `destructive`

Example:

```jinja2
{% load projectify %}
TODO
```

## icon

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

## User avatar

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
<div class="shrink-0 flex flex-row h-6 w-6 items-center rounded-full border border-primary bg-base-200"></div>
```
