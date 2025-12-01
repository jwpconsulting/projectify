---
title: Backend template tags guide
---

This is a guide for using the Projectify's Django template tags.
You can find the source code for the template tags in
`backend/projectify/templatetags/projectify.py`

# Percent

Formats a value as a percentage. Example:

```jinja
{% percentage 100 %}
```

Renders to

```html
TODO
```

# Anchor

Create an anchor with Tailwind styling. Usage:

```html
{% anchor href="/" label=_("Learn more") external=True %}
```

This renders to the following. The styling is subject to change.

```html
<a href="/"
   class="text-primary underline hover:text-primary-hover active:text-primary-pressed text-base"
   target="_blank"
  >Learn more<
  span class="sr-only">(Opens in new tab)</span>
  <svg ...></svg>
</a>
```

You can also remove `external=True`, or instead set `external=False`:

```html
{% anchor href="/" label=_("Learn more") %}
```

This renders to the following:

```html
<a href="/"
   class="text-primary underline hover:text-primary-hover active:text-primary-pressed text-base"
   target="_blank"
  >Learn more</a>
```

# User avatar

Render a user avatar using the `user_avatar` template tag:

```jinja
{% user_avatar user %}
```

If the user has a picture set, it renders to the following:

```html
<div class="..."><img src="..." alt="user's preferred name"></div>
```

If there's not picture, it renders the following:

```html
<div class="shrink-0 flex flex-row h-6 w-6 items-center rounded-full border border-primary bg-base-200"></div>
```
