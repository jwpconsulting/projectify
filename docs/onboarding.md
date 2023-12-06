# Onboarding

These are the onboarding steps:

- _About you_: `/onboarding/about-you`
- _New workspace_: `/onboarding/new-workspace`
- _New workspace board_: `/onboarding/new-workspace-board/[workspaceUuid]`
- _New task_: `/onboarding/new-task/[workspaceBoardUuid]`
- _New label_: `/onboarding/new-label/[taskUuid]`
- _Assign task (confirmation)_: `/onboarding/assign-task/[taskUuid]`

## Design and implementation criteria

Necessary criteria:

- Does not frustrate the user by being long and wordy
- Explain everything the user needs to know to get started working
- Allow onboarding process to be continued after an interruption, such as
  browser restart, server crash, ...
- Work well on small screens

Bonus criteria:

- Have satisfying eye candy

## New onboarding steps

When a user signs up for Projectify, we have to make them aware of

- the things that they can do, now that they have signed up,
- what the onboarding process will look like,
- Projectify being in trial mode unless they subscribe, and
- how to subscribe

We need a welcome page that summarizes what Projectify is and what the user
can do with it, and what the trial encompasses.

It is important to explain to the user at the end of the onboarding
how to upgrade from trial mode. In the future, it could also be helpful
to point them to various starter resources like FAQs or help pages.

The onboarding steps should be:

- Welcome: /onboarding/welcome
- About you: /onboarding/about-you
- New workspace: /onboarding/new-workspace
- New workspace board: /onboarding/new-workspace-board
- New task: /onboarding/new-task
- New label: /onboarding/new-label
- Assign task: /onboarding/assign-task

Furthermore, after _New workspace board_, the user should be able to skip the
onboarding and go directly to the newly created workspace board. It is
not possible at the moment to skip workspace board creation, since that
would make the UI look pretty awkward; the dashboard does not correctly
render when no workspace board is selected.

### Welcome

The welcome onboarding page is the first page a user sees after logging in and
not added to any workspace. (no workspace user exists for this user) Here,
we explain to the user that:

- They have successfully signed up and logged in on Projectify
- In the following steps, they will perform the necessary data entry to get
  started using Projectify
- They can use Projectify for free in trial mode, with certain restrictions.

### About you

The about you page allows us to learn more about the user. For now, we will
only ask them to enter their preferred name, if they want to. They can
also go ahead without entering a preferred name. We explain to them, that
the preferred name will be used when showing that a task has been assigned to
them and in other parts of Projectify as well to indicate that something is
relevant to the user.

### New workspace

Without a workspace, there are no meaningful actions a user can perform in
Projectify. In this step, we ask the user to provide a name for the workspace
that they want to create. We create the workspace and automatically assign
the user as the workspace's owner.

If a workspace already exists, we tell them that they may continue setting
up this workspace instead of creating a new one. A link is shown that brings
them to the next onboarding step (workspace board creation) for the already
existing workspace.

### New workspace board

After a workspace has been created, the user is now asked to specify the name
for a workspace board that we will create for them.

Again, should the user already have created a workspace board, they can
continue from this step directly with Projectify telling the user that
they have already created a workspace board and asking them whether they want
to continue using it in the next step.

### New task

We assume that the user wants to try putting their first task in this workspace
board, so we create a workspace board section "To Do" for them, and ask them
what they want their task to be.

If a task has been created before, it should support continuation. This is
not implemented at the time of writing. (2023-12-06)

The task will be automatically assigned to them.

### New label

Here, we create a new label that will be assigned to the newly created task
in the previous step.

Bug: If a label has already been created (in a previous onboarding run), the
user might try to create a label with the same name. This will lead to a 500
error in the backend at the time of writing. (2023-12-06) There is an issue
with a unique constraint for workspace and label name, which has to be
resolved.

### Assign task

With the newly created task, now equipped with a label, we tell the user that
it has been assigned to them, and that they can now get started using
Projectify.

Furthermore, we reiterate that the user is currently using their Projectify
workspace in trial mode, and guide them to where they can activate a
subscription in the workspace settings.

We also direct the user to a contact page where they can ask for help, with
either the onboarding, or any issues or questions they encounter when using
the Projectify dashboard.
