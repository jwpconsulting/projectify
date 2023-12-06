# Onboarding

These are the onboarding steps:

- _About you_: `/onboarding/about-you`
- _New workspace_: `/onboarding/new-workspace`
- _New workspace board_: `/onboarding/new-workspace-board/[workspaceUuid]`
- _New task_: `/onboarding/new-task/[workspaceBoardUuid]`
- _New label_: `/onboarding/new-label/[taskUuid]`
- _Assign task (confirmation)_: `/onboarding/assign-task/[taskUuid]`

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
- Final steps: /onboarding/final-steps

Furthermore, after _New workspace board_, the user should be able to skip the
onboarding and go directly to the newly created workspace board. It is
not possible at the moment to skip workspace board creation, since that
would make the UI look pretty awkward; the dashboard does not correctly
render when no workspace board is selected.
