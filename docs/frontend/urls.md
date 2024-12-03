<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# URLs for prerendered pages

Useful when testing on localhost. Generate with

```bash
npm run build && find build -name '*.html' | sed \
  -e 's/build/- http:\/\/localhost:3000/' \
  -e 's/.html//' \
  -e '/fallback/d' \
  -e '/index/d'
```

- http://localhost:3000/free-software
- http://localhost:3000/accessibility
- http://localhost:3000/help
- http://localhost:3000/security/disclose
- http://localhost:3000/security/general
- http://localhost:3000/pricing
- http://localhost:3000/solutions/development-teams
- http://localhost:3000/solutions/remote-work
- http://localhost:3000/solutions/research
- http://localhost:3000/solutions/academic
- http://localhost:3000/solutions/personal-use
- http://localhost:3000/solutions/project-management
- http://localhost:3000/user/requested-password-reset
- http://localhost:3000/user/sent-email-confirmation-link
- http://localhost:3000/user/log-out
- http://localhost:3000/user/reset-password
- http://localhost:3000/contact-us
- http://localhost:3000/tos
- http://localhost:3000/ethicalads
- http://localhost:3000/credits
- http://localhost:3000/privacy
- http://localhost:3000/help/trial
- http://localhost:3000/help/tasks
- http://localhost:3000/help/billing
- http://localhost:3000/help/filters
- http://localhost:3000/help/basics
- http://localhost:3000/help/sections
- http://localhost:3000/help/projects
- http://localhost:3000/help/workspaces
- http://localhost:3000/help/team-members
- http://localhost:3000/help/roles
- http://localhost:3000/help/quota
- http://localhost:3000/help/labels
- http://localhost:3000/solutions

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
