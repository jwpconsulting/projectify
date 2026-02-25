---
title: Projectify Architecture
author: Justus Perlwitz
date: 2024-03-18
updated: 2026-02-20
---

<!--
SPDX-FileCopyrightText: 2024,2026 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

This document describes the software architecture of the Projectify software.
It was written with a deployment on Render in mind, so certain parts might
change when deployed on a different infrastructure.

The Projectify software is implemented using Django.

# General run time requirements

To use Projectify, users need a computer that meets the following criteria:

1. Run a modern browser that can run a recent version of ECMAScript.
2. Have a stable internet connection to the Projectify domains.
3. Provide a modest amount of computing resources (imagine a laptop computer from 2010).

The Projectify software has the following requirements for its runtime:

1. Provide a PostgreSQL database instance,
2. Provide a modest amount of computing resources, and
3. Have a reliable and fast (more than 1 Gbit per second) internet connection
   to its users.

# Components

Projectify uses Django [^django] with PostgreSQL version 15.5 [^postgresql] and higher.
To connect to PostgreSQL instances, Projectify uses Psycopg version 3 [^psycopg].

The frontend templates use HTMX [^htmx] and Tailwind CSS [^tailwind] is used.

The style guide for this Django Project derives from the HackSoftware
Django-Styleguide [^django-styleguide]. This is not always strictly enforced, but roughly,

- selectors,
- services,
- APIViews with integrated Serializers,
- Thin models with no or minimal Managers

are used. Since the transition to the Django-Styleguide came late in the
project, not every part of the backend is written this way.

To validate user authorization, Projectify uses django-rules [^django-rules].

# API Security

For API Security, we want to prevent users from performing actions that they
are not authorized to do, accessing information that they are not allowed to
see. We want to prevent unauthorized persons from being able to impersonate a
registered user, or disturb other users from using the Projectify software.

Authorization validation happens as part of a call to a service function in the
backend. Further optical validation, such as disabling or hiding functionality
in the frontend templates is not relevant to API security. Authorization checking also
involves validating quotas, such as ensuring that a workspace can not have too
many team members added.

Roughly, the steps required, from accessing Projectify in the browser to successful authorization, are as follows:

1. The User initiates an action in their browser, such as adding a new task.
2. The browser sends a POST request to the backend. This request contains the user's session id cookie.
3. The backend receives the request. It validates that the session ID is valid.
   This means that the session ID is signed correctly, not expired, not
   removed in the backend's session table, and that it points to an existing user.
4. The create task view `task_create` in `projectify/workspace/views/task.py` de-serializes the contents of the request using a Django Form.
   As
   part of the de-serialization, the backend checks whether the user is allowed
   to access the workspace and sections for this task
    A user can only access a workspace that they are a team member of.
5. The create task view passes the validated data to the task creation service method
   `task_create` in `projectify/workspace/services/task.py`.
6. The task creation service method validates the user's permissions and thus establishes
   that they are authorized to create a task for this workspace.
7. Now task creation service method creates the task and the backend returns
a confirmation page to the browser.

In the case of a missing or invalid session cookie, the above flow would fail
at step 3, since the APIView requires authenticated users.

In the case of a team member with insufficient permission to create a task
within their workspace, the above flow would fail at step 6. The workspace
itself can be accessed by them, and the view code will run correctly, until the
service method is called from within where the authorization validation will
throw an exception.

Should a logged in user not be authorized to access a specific workspace, the
above flow will fail at step 4, since the workspace they request for a task to
be created in is not accessible by them.

# Performance

In terms of performance, Projectify has several goals:

- Projectify shall work acceptably with slow internet connections. (high
  latency, low bandwidth)
- Projectify shall work acceptably with slow computers and browsers. (low available working
  memory, low CPU resources)
- Projectify shall work acceptably when run on a low-spec server used to run
  the backend.
- Projectify shall work acceptably with large workspace and project sizes.
- Projectify shall work acceptably with many users interacting with a
  workspace.
- Projectify shall handle many connections in the backend simultaneously, and
  speedily return responses to requests.

# Reliability

To keep the Projectify software reliable and trustworthy, it shall be designed
according to the following criteria:

- The Projecitfy backend shall prevent bugs from corrupting user state.
- Projectify shall prevent users from inadvertently destroying or modify data.

[^htmx]: [</> htmx - high power tools for HTML](https://htmx.org/) *htmx.org*
[^tailwind]: [Tailwind CSS](https://tailwindcss.com) *tailwindcss.com*
[^django]: [The web framework for perfectionists with deadlines - Django](https://www.djangoproject.com/) *www.djangoproject.com*
[^postgresql]: [PostgreSQL: The World's Most Advanced Open Source Relational Database](https://www.postgresql.org) *www.postgresql.org*
[^psycopg]: [PostgreSQL driver for Python — Psycopg](https://www.psycopg.org) *www.psycopg.org*
[^django-styleguide]: [Django styleguide used in HackSoft projects](https://github.com/HackSoftware/Django-Styleguide) *github.com/HackSoftware/Django-Styleguide*
[^django-rules]: [Awesome Django authorization, without the database](https://github.com/dfunckt/django-rules) *github.com/dfunckt/django-rules*
