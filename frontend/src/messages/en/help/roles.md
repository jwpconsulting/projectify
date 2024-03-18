Roles can be assigned to team members within a workspace by going to the
[workspace settings](/help/team-members#edit-a-team-members-permissions).
In this document, you will learn the different available roles and what
permissions are included in a role.

# Available roles

There are 4 different roles available to be assigned to a team member. They
are listed here starting with the role with the fewest permissions:

1. Observer
2. Contributor
3. Maintainer
4. Owner

That means that owners have the most permissions, and observers have the least.
You can assign team members in your workspace a role that suits the
activities that they will perform on your workspace. To better explain what
roles can do, it is important to understand the available resources in a
workspace.

The resources and their contained information that team members can perform
actions are as follows:

| Resource                    | Contains information such as                                |
| --------------------------- | ----------------------------------------------------------- |
| Workspace                   | Title and description                                       |
| Workspace billing settings  | Current subscription status and payment information         |
| Team members and invites | Who has been added to the workspace, and who is invited     |
| Project                     | Description and other information about a project           |
| Sections                    | Name, position within project                               |
| Tasks                       | Title, description, due date, label, assignee, and position |
| Sub tasks                   | Done state and title                                        |
| Labels                      | Name and color                                              |

# Overview

The following is a quick overview over all permissions. Each role's permissions
are further described in the individual sections below. The meaning of an
individual cell in this table is as follows:

- **Read** indicates that a team member with this role can view the
  resource, but not make any changes to it
- **Write** indicates that a team member with this role can create, view,
  and update the resource, but not delete it.
- **Full** indicates that a team member with this role can view, update and
  delete the resource.
- Cells with a **-** indicate that no permissions exist for this resource and
  role.

| Resource                    | Observer | Contributor | Maintainer | Owner |
| --------------------------- | -------- | ----------- | ---------- | ----- |
| Workspace                   | Read     | Read        | Read       | Full  |
| Workspace billing settings  | -        | -           | -          | Full  |
| Team members and invites | Read     | Read        | Read       | Full  |
| Project                     | Read     | Read        | Full       | Full  |
| Sections                    | Read     | Read        | Full       | Full  |
| Tasks                       | Read     | Write       | Full       | Full  |
| Sub tasks                   | Read     | Full        | Full       | Full  |
| Labels                      | Read     | Read        | Full       | Full  |

# Observer

**Observer** team members can view almost all available resources, except
for workspace billing settings. They can not create, update, or delete any of
the other resources. This role is suitable for outside users who want to
observer the progress of a project, but do not need to commit any changes
themselves.

# Contributor

On top of the **observer** permissions, a **contributor** team member has the
following additional permissions in their workspace:

- They can create and update tasks
- They can create, update and delete sub tasks

More importantly, they do not gain any additional delete permissions for the
above two resources, or any other edit permissions for projects,
sections, labels, users, billing settings, and the workspace itself.

# Maintainer

With the **maintainer** team member role, the following activities become
possible, on top of the **contributor** permissions:

- Create, update and delete projects
- Create, update and delete sections
- Create, update and delete labels
- Delete tasks

# Owner role

With the **owner** team member role, a user gains the following permissions
on top of the **maintainer** permissions:

- Update or delete the workspace
- Update billing settings
- Invite team members, update their information and remove them

# Choosing the right role

Depending on what activities a team member will perform, you can choose the
correct role for them. Not every team member will need the same access to
all resources, and this can often prevent accidental deletion of important
data.

Review the available roles and their permissions above and go to the workspace
settings to assign them to a team member. For more information on how to do
this, please refer to the [team members help
page](/help/team-members#edit-a-team-members-permissions).
