# Workspace member settings

Here is some code that was removed from the member settings page and could be
useful again at some point

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
