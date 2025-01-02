---
title: Projectify Architecture
author: Justus Perlwitz
date: 2024-03-18
---

<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

This document describes the software architecture of the Projectify software.
It was written with a deployment on Heroku in mind, so certain parts might
change when deployed on a different infrastructure.

The Projectify software is divided into two main parts that in turn interface
with external components. These two parts are a

- frontend, being executed in the browser by a Projectify user, and a
- backend, serving requests made by the frontend.

# General run time requirements

The frontend relies on

- a browser being able to run a recent version of ECMAScript (basically
  JavaScript, but with more standardization),
- a stable internet connection to the backend, and asset storage, and
- a modest amount of computing resources (imagine a laptop computer from 2010).

The backend requires

- a PostgreSQL database instance,
- a Redis instance (for queuing, caching, and WebSocket connections),
- a modest amount of computing resources, and
- reliable connectivity to the wherever a frontend is run,

# Frontend components

The frontend is implemented using SvelteKit[^1]. SvelteKit is a frontend
application framework that in turn is powered by Svelte[^2].

In order to communicate with the backend, the frontend uses a combination of
fetch [^3] requests and WebSocket. For WebSocket, a library called Sarus [^3]
is used.

To style the frontend, Tailwind CSS [^4] is used.

There are dozens of helper libraries used in the frontend as well, so a look at
`frontend/package.json` under `dependencies` will show what else is used.

# Backend components

The backend is implemented in Django [^5] and Django REST Framework [^6].
Asynchronous WebSocket communication is enabled using Django Channels [^7].

For the DBMS PostgreSQL version 15.5 [^8] and higher is used and supported. To
connect to a PostgreSQL instance, Psycopg version 3 [^9] is used.

The style guide for this Django Project is derived from the HackSoftware
Django-Styleguide [^10]. This is not always strictly enforced, but roughly,

- selectors,
- services,
- APIViews with integrated Serializers,
- Thin models with no or minimal Managers

are used. Since the transition to the Django-Styleguide came late in the
project, not every part of the backend is written this way.

In order to validate authorization, rules [^11] is used.

# API Security

For API Security, we want to prevent users from performing actions that they
are not authorized to do, accessing information that they are not allowed to
see. We want to prevent unauthorized persons from being able to impersonate a
registered user, or disturb other users from using the Projectify software.

Authorization validation happens as part of a call to a service function in the
backend. Further optical validation, such as disabling or hiding functionality
in the frontend is not relevant to API security. Authorization checking also
involves validating quotas, such as ensuring that a workspace can not have too
many team members added.

Roughly, flow from frontend to successful authorization is as follows:

1. User initiates action in frontend, such as adding a new task
2. The frontend initiates a POST request to the backend's create task endpoint.
   This request contains the user's session id cookie.
3. The backend receives the request. It validates that the session id is valid,
   which means that the session id is signed correctly, not expired, not
   removed in the backend's session table, and points to an existing user.
4. The create task APIView de-serializes the contents of the request, and as
   part of the de-serialization, workspace and section used for this task are
   retrieved and validated to be accessible by the authenticated user. A user
   can only access a workspace that they are a team member of.
5. The task creation data is passed to the task creation service method.
6. The service method validates the user's permissions and thus establishes
   that they are authorized to create a task for this workspace.
7. Now the task is created, and a successful status code is returned to the
   frontend.

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
- Projectify shall work acceptably with slow computers. (low available working
  memory, low CPU resources) used to run the frontend
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

- A bug in the frontend shall never cause state in the backend to become
  invalid
- The frontend shall fail in the gentlest way possible when no connection can
  be established with the backend
- No interaction in the frontend shall inadvertently destroy or modify data,
  against the intentions of a user
- The frontend shall crash in gentle ways, and the user interface shall always
  guide the user to restart or reset the frontend to a known good state

[^1]: SvelteKit: https://kit.svelte.dev/

[^2]: Svelte: https://svelte.dev/

[^3]: Sarus: https://github.com/anephenix/sarus/

[^4]: Tailwind CSS: https://tailwindcss.com/

[^5]: Django: https://www.djangoproject.com/

[^6]: Django REST Framework: https://www.django-rest-framework.org/

[^7]: Django Channels: https://channels.readthedocs.io/en/latest/

[^8]: PostgreSQL: https://www.postgresql.org/

[^9]: Psycopg: https://www.psycopg.org/

[^10]: Django-Styleguide: https://github.com/HackSoftware/Django-Styleguide

[^11]: rules: https://github.com/dfunckt/django-rules
