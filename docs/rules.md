# Rules

Projectify uses roles within a workspace to grant users privileges to do
certain things.

There are four roles, sorted by least privileged role first

- Observer
- Contributor
- Maintainer
- Owner

The resources that workspace users can work on are the following:

- Workspace
- Workspace user invite
- Workspace user
- Project
- Section
- Task
- Label
- Task label
- Sub task
- Chat message
- Customer

The following actions are possible on each resource, modelled after a typical
CRUD application:

- Create
- Read
- Update
- Delete

## Overview

In the following table you can see, for each resource and action, the minimum
role required to perform that action.

| Resource                | Create     | Read       | Update     | Delete     |
|-------------------------|------------|------------|------------|------------|
| Workspace               | Owner      | Observer   | Owner      | Owner      |
| Workspace user invite   | Owner      | Owner      | Owner      | Owner      |
| Workspace user          | Owner      | Observer   | Owner      | Owner      |
| Project         | Maintainer | Observer   | Maintainer | Maintainer |
| Section | Maintainer | Observer   | Maintainer | Maintainer |
| Task                    | Contributor     | Observer   | Contributor     | Maintainer |
| Label                   | Maintainer | Observer   | Maintainer | Maintainer |
| Task label              | Contributor     | Observer   | Contributor     | Contributor     |
| Sub task                | Contributor     | Observer   | Contributor     | Contributor     |
| Chat message            | Contributor     | Observer   | Contributor     | Maintainer |
| Customer                | Owner      | Owner      | Owner      | Owner      |

## Role descriptions

### Observer

The idea of __observer__ workspace users is to grant third parties, such as
persons observing a project but not directly participating in them, to see how
a project is doing.

An observer can only read resources in their workspace, but not perform any
changes on them or create them. They can read the following resources:

- Workspace
- Workspace users
- Projects
- Sections
- Tasks
- Labels
- Task labels
- Sub tasks
- Chat messages

### Contributor

A workspace user __contributor__ is an individual contributor in a team.

In addition to an observer's permissions, contributors have the following additional
permissions:

- A contributor can create and update tasks
- A contributor can create, update and delete task labels, that is, they can assign
  labels to tasks
- A contributor can create, update and delete sub tasks.
- A contributor can create and update chat messages.

### Maintainer

A workspace __maintainer__ is someone who manages the state of projects of
their team and therefore has to organize and clean up their team's project data
on Projectify. Persons with this role are typically called Project Manager,
Project Lead, and so on.

Maintainer have the following permissions in addition to contributor permissons:

- Create, update and delete projects
- Create, update and delete sections
- Delete tasks
- Create, update and delete labels
- Delete chat messages

### Owner

A workspace __owner__ is a system or billing administrator, taking care of
organization's Projectify workspace's overall state.

They have the following additional permissions, necessary for billing and
workspace maintenance.

- Create, update and delete workspaces
- Create, read, update and delete workspace user invites, that is, invite new
  workspace users
- Create, update and delete workspace users
- Create, read, update and delete customer

## Rule implementation

In the __backend__ we validate role permissions during each API request coming
in. Since a role is tied to the WorkspaceUser object, we reference the
authenticated user's account and the workspace they are operating on to get the
WorkspaceUser instance.

The workspace is inferred from the actual resource the user is calling the API
on. For example, when updating a section, we resolve the
workspace belonging to it by looking at the associated project's
workspace foreign key. The order of lookup operations is roughly:

1. Identify current, authenticated user based on session cookie
2. Identify resource based on API URL (project/<uuid>/... would be
   workspace with UUID <uuid>)
3. For the authenticated user, look up all available resources of the given
   type. (For projects, retrieve all projects that they can
   access as a workspace user)
4. See if resource is part of the available resources (For projects,
   match by <uuid>)
5. If no resource is found, return HTTP status code 404 __NOT FOUND__.
6. For a GET, we are done and can serialize return the resource (except for
   workspace user invites)
7. For POST/PUT/DELETE, we now reference the workspace user record (M2M mapping
   between authenticated user and the workspace containing the resource), and
   check if they have permission to perform the operation.
8. If a workspace is in trial mode, we apply some extra logic here on top of
   permission checking.

Trial mode checking adds more complexity to this, but essentially only
restricts an action based on whether a workspace is within trial limits. Trial
limits are defined as a workspace only being able to have a finite amount of
individual resources. For example, there currently is a limit of 2 of workspace
users and workspace user invites.


