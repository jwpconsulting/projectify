<script lang="ts">
    import { page } from "$app/stores";
    import { browser } from "$app/environment";
    import {
        currentWorkspace,
        currentWorkspaceUuid,
        setAndNavigateWorkspaceBoard,
    } from "$lib/stores/dashboard";
    $: {
        if ($currentWorkspace) {
            if (
                $currentWorkspace.workspace_boards &&
                $currentWorkspace.workspace_boards.length
            ) {
                setAndNavigateWorkspaceBoard(
                    $currentWorkspace.workspace_boards[0].uuid
                );
            } else {
                throw new Error("No workspace board");
            }
        }
    }
    $: {
        if (browser) {
            $currentWorkspaceUuid = $page.params["workspaceUuid"];
        }
    }
</script>
