<script lang="ts">
    import { browser } from "$app/environment";
    import {
        currentWorkspace,
        setAndNavigateWorkspaceBoard,
        setFirstWorkspace,
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
    if (browser) {
        setFirstWorkspace();
    }
</script>
