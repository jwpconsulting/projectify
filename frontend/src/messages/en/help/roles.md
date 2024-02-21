Roles can be assigned to workspace users within a workspace by going to the
[workspace settings](/help/workspace-users#edit-a-workspace-users-permissions).
In this document, you will learn the different available roles and what
permissions are included in a role.

# Available roles

There are 4 different roles available to be assigned to a workspace user. They
are listed here starting with the role with the fewest permissions:

1. Observer
2. Member
3. Maintainer
4. Owner

That means that owners have the most permissions, and observers have the least.
You can assign workspace users in your workspace a role that suits the
activities that they will perform on your workspace. To better explain what
roles can do, it is important to understand the available resources in a
workspace.

The resources and their contained information that workspace users can perform
actions are as follows:

| Resource                    | Contains information such as                                |
| --------------------------- | ----------------------------------------------------------- |
| Workspace                   | Title and description                                       |
| Workspace billing settings  | Current subscription status and payment information         |
| Workspace users and invites | Who has been added to the workspace, and who is invited     |
| Workspace board             | Description and other information about a workspace board   |
| Workspace board sections    | Name, position within workspace board                       |
| Tasks                       | Title, description, due date, label, assignee, and position |
| Sub tasks                   | Done state and title                                        |
| Labels                      | Name and color                                              |

# Overview

The following is a quick overview over all permissions. Each role's permissions
are further described in the individual sections below. The meaning of an
individual cell in this table is as follows:

- **Read** indicates that a workspace user with this role can view the
  resource, but not make any changes to it
- **Write** indicates that a workspace user with this role can create, view,
  and update the resource, but not delete it.
- **Full** indicates that a workspace user with this role can view, update and
  delete the resource.
- Cells with a **-** indicate that no permissions exist for this resource and
  role.

| Resource                    | Observer | Member | Maintainer | Owner |
| --------------------------- | -------- | ------ | ---------- | ----- |
| Workspace                   | Read     | Read   | Read       | Full  |
| Workspace billing settings  | -        | -      | -          | Full  |
| Workspace users and invites | Read     | Read   | Read       | Full  |
| Workspace board             | Read     | Read   | Full       | Full  |
| Workspace board sections    | Read     | Read   | Full       | Full  |
| Tasks                       | Read     | Write  | Full       | Full  |
| Sub tasks                   | Read     | Full   | Full       | Full  |
| Labels                      | Read     | Read   | Full       | Full  |

# Observer

**Observer** workspace users can view almost all available resources, except
for workspace billing settings. They can not create, update, or delete any of
the other resources. This role is suitable for outside users who want to
observer the progress of a project, but do not need to commit any changes
themselves.

# Member

On top of the **observer** permissions, a **member** workspace user has the
following additional permissions in their workspace:

- They can create and update tasks
- They can create, update and delete sub tasks

More importantly, they do not gain any additional delete permissions for the
above two resources, or any other edit permissions for workspace boards,
sections, labels, users, billing settings, and the workspace itself.

# Maintainer

With the **maintainer** workspace user role, the following activities become
possible, on top of the **member** permissions:

- Create, update and delete workspace boards
- Create, update and delete workspace board sections
- Create, update and delete labels
- Delete tasks

# Owner role

With the **owner** workspace user role, a user gains the following permissions
on top of the **maintainer** permissions:

- Update or delete the workspace
- Update billing settings
- Invite workspace users, update their information and remove them

# Choosing the right role

Depending on what activities a workspace user will perform, you can choose the
correct role for them. Not every workspace user will need the same access to
all resources, and this can often prevent accidental deletion of important
data.

Review the available roles and their permissions above and go to the workspace
settings to assign them to a workspace user. For more information on how to do
this, please refer to the [workspace users help
page](/help/workspace-users#edit-a-workspace-users-permissions).
