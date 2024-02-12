# Layouts in this application

Assuming all paths relative to `src/routes`.

- `+layout.ts`: Base layout
- `(platform)/dashboard/task/[taskUuid]/+layout.ts`: Layout for task CRUD
- `(platform)/dashboard/workspace/[workspaceUuid]/+layout.ts`: Layout for
  workspace loading (redirect to ws board) and settings
- `(platform)/dashboard/workspace-board/[workspaceBoardUuid]/+layout.ts`: Layout for
  workspace board view (the main view in this application)
- `(platform)/dashboard/workspace-board-section/[workspaceBoardUuid]/+layout.ts`: Layout for
  workspace board section view for task creation, redirecting to ws board
  scrolled to section
- `(platform)/+layout.ts`: Layout for logged in users
- `(storefront)/(auth)/+layout.ts: Layout for non-logged in users
- `(onboarding)/+layout.ts`: Layout for logged in users going through
  onboarding

# `(platform)/+layout.ts`

Every page here will automatically have a side nav. Since onboarding should not
show a side nav, a recent change was to move onboarding into its own layout
group.
