# Workspace user settings

Here is some code that was removed from the workspace user settings page and
could be useful again at some point. We renamed member to workspace user, so
some of the code below has to be adjusted accordingly.

```typescript
async function onNewMember() {
  if (!modalRes.outputs?.email) {
    goto("/billing");
    return;
  }
  if (!$currentWorkspace) {
    return;
  }
  await client.mutate({
    mutation: Mutation_AddUserToWorkspace,
    variables: {
      input: {
        uuid: $currentWorkspace.uuid,
        email: modalRes.outputs.email,
      },
    },
  });
}
async function onRemoveUser(workspaceUser: WorkspaceUser) {
  if (!$currentWorkspace) {
    return;
  }
  await client.mutate({
    mutation: Mutation_RemoveUserFromWorkspace,
    variables: {
      input: {
        uuid: $currentWorkspace.uuid,
        email: workspaceUser.user.email,
      },
    },
  });
}

async function onEditUser(workspaceUser: WorkspaceUser) {
  if (!$currentWorkspace) {
    return;
  }
  await client.mutate({
    mutation: Mutation_UpdateWorkspaceUser,
    variables: {
      input: {
        workspaceUuid: $currentWorkspace.uuid,
        email: modalRes.outputs.email,
        role: modalRes.outputs.role,
        jobTitle: modalRes.outputs.job_title || "",
      },
    },
  });
}
```
