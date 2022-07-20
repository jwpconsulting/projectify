<script lang="ts">
    import { getWorkspaces, getWorkspace } from "$lib/repository";
    import { getDashboardWorkspaceBoardUrl } from "$lib/urls";
    import { browser } from "$app/env";
    import {
        currentWorkspaceUuid,
        currentWorkspaceBoardUuid,
    } from "$lib/stores/dashboard";
    import { goto } from "$app/navigation";

    async function fetch() {
        const workspaces = await getWorkspaces();
        let workspaceUuid;
        if (workspaces.length) {
            workspaceUuid = workspaces[0].uuid;
        } else {
            throw new Error("No workspaces");
        }
        const workspace = await getWorkspace(workspaceUuid);
        let workspaceBoardUuid;
        if (workspace.workspace_boards && workspace.workspace_boards.length) {
            workspaceBoardUuid = workspace.workspace_boards[0].uuid;
        } else {
            throw new Error("No workspace board");
        }
        currentWorkspaceUuid.set(workspace.uuid);
        currentWorkspaceBoardUuid.set(workspaceBoardUuid);
        goto(getDashboardWorkspaceBoardUrl(workspaceBoardUuid));
    }
    if (browser) {
        fetch();
    }
</script>
