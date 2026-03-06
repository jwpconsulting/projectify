<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Django show_urls

Use `uv run ./manage.py show_urls` to show all URLs that Projectify recognizes:

```bash
uv run ./manage.py show_urls | grep -v admin
```

```
/	projectify.storefront.views.index	storefront:landing
/.well-known/security.txt	django.views.generic.base.TemplateView
/403.html	projectify.views.handler403
/404.html	projectify.views.handler404
/500.html	projectify.views.handler500
[…]
/accessibility	projectify.storefront.views.accessibility	storefront:accessibility
/contact-us	projectify.storefront.views.contact_us	storefront:contact_us
/corporate/stripe-webhook/	projectify.corporate.views.stripe.stripe_webhook	corporate:stripe-webhook
/credits	projectify.storefront.views.credits	storefront:credits
/dashboard/	projectify.workspace.views.dashboard.redirect_to_dashboard	dashboard:dashboard
/dashboard/avatar/<uuid:team_member_uuid>.svg	projectify.workspace.views.avatar_marble.avatar_marble_view	dashboard:avatar-marble
/dashboard/project/<uuid:project_uuid>	projectify.workspace.views.project.project_detail_view	dashboard:projects:detail
[…]
/download	projectify.storefront.views.download	storefront:download
/ethicalads	projectify.storefront.views.ethicalads	storefront:ethicalads
/free-software	projectify.storefront.views.free_software	storefront:free_software
/healthz	projectify.views.health_check	health-check
/help/	projectify.help.views.help_list	help:list
/help/basics	projectify.help.views.help_detail	help:topic:basics
[…]
/onboarding/	django.views.generic.base.RedirectView	onboarding:welcome
/onboarding/about-you	projectify.onboarding.views.about_you	onboarding:about_you
[…]
/solutions/development-teams	projectify.storefront.views.solutions_development_teams	storefront:solutions:development_teams
/solutions/project-management	projectify.storefront.views.solutions_project_management	storefront:solutions:project_management
/tos	projectify.storefront.views.tos	storefront:tos
/user/confirm-email/<str:email>/<str:token>	projectify.user.views.auth.email_confirm	users:confirm-email
/user/confirm-password-reset/<str:email>/<str:token>	projectify.user.views.auth.password_reset_confirm	users:confirm-password-reset
/user/log-in	projectify.user.views.auth.log_in	users:log-in
[…]
/user/sign-up	projectify.user.views.auth.sign_up	users:sign-up
```

# Thoughts on URLs for Projectify

A page can serve various purposes. Some of which are:

- Read a record
- Read multiple records at once
- Create, update and delete records
- Request an operation
- Show the result of an operation

I suggest the following base name for each of the three above activities:

`$PREFIX` can denote anything that comes in front of the URL, such as a group
identifier. This comes in handy when a record has to be identified as part of
other identifiers.

# Reading a record

If we read a record with name `<record-name>`, and we access it by specifying
an identifier such as a UUID <uuid>, we use a URL like

```
$PREFIX/<record-name>/<uuid>
```

# Reading multiple records

For multiple records of name `<record-name>`, we access them like so:

```
$PREFIX/<record-name/
```

# Create records

For this, we present a page with a URL such as

```
$PREFIX/<record-name>/create
```

Here it could be handy to have the prefix denote a collection in which this
record shall be created. For example, the URL could be

```
┌───────────────────────────┐ ┌───────────────┐ ┌──────┐
│workspaces/<workspace-uuid>│/│workspace-board│/│create│
└──────────┬────────────────┘ └─────┬─────────┘ └──┬───┘
           ▼                        ▼              ▼
        $PREFIX                 <record-name>    create
                                                 page
```

# Update records

For this, we present a page with a URL such as

```
$PREFIX/<record-name/<uuid>/update
```

# Delete records

If a specific deletion confirmation page is needed, it could be accessed using
the following URL:

```
$PREFIX/<record-name>/<uuid>/delete
```

Perhaps, if a result page is needed, it could look like this

```
$PREFIX/<record-name>/deleted
```

# Requesting an operation

This is, for example, relevant during user signup. When a user wants to confirm
their email, we generate a URL similar to this:

```
user/confirm-email/<email>/<token>
```

Aside: It would be nice to be able to POST email and token somehow instead,
that way we can't leave them in our server logs accidentally.

The idea is to present a verb-noun combination such as in this case
`confirm-email`. We choose not to name it `email-confirmation`, which sounds
like an equally valid option -- but we stick with verb-noun this time.

The general schema is:

```
$PREFIX/<do-something-with>-<resource>
```

# Show the result of an operation

Similar to how we have described with deletion confirmation above, we combine a
past tense verb and a resource name. To show the user that we have sent them an
email confirmation link, we redirect them to a URL like this:

```
user/sent-email-confirmation-link
```

The general schema is

```
$PREFIX/<did-something-with>-<resource>
```

In the case of the deletion above, since the resource name is already implied
in the path, we can then just stick to a schema like so:

```
$PREFIX/<resource-name>/<did-something-with>
```
