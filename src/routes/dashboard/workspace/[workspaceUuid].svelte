<script lang="ts">
    import { page } from "$app/stores";
    import { getWorkspace } from "$lib/repository";
    import { browser } from "$app/env";
    import { getDashboardWorkspaceBoardUrl } from "$lib/urls";
    import { goto } from "$app/navigation";
    import { currentWorkspace, currentBoardUuid } from "$lib/stores/dashboard";

    async function fetch() {
        const workspaceUuid = $page.params["workspaceUuid"];
        if (!workspaceUuid) {
            throw new Error("Expected workspaceUuid");
        }
        const workspace = await getWorkspace(workspaceUuid);
        let workspaceBoardUuid;
        if (workspace.workspace_boards && workspace.workspace_boards.length) {
            workspaceBoardUuid = workspace.workspace_boards[0].uuid;
        } else {
            throw new Error("No workspace board");
        }
        currentWorkspace.set(workspace);
        currentBoardUuid.set(workspaceBoardUuid);
        goto(getDashboardWorkspaceBoardUrl(workspaceBoardUuid));
    }
    if (browser) {
        fetch();
    }
</script>
