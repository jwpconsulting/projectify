<script lang="ts">
    import { Archive, Pencil } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import { archiveWorkspaceBoard } from "$lib/repository/workspace/workspaceBoard";
    import {
        openConstructiveOverlay,
        openDestructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { ConstructiveOverlayType } from "$lib/types/ui";
    import type { WorkspaceBoard } from "$lib/types/workspace";

    export let workspaceBoard: WorkspaceBoard;

    async function editBoard() {
        // open constructive dialog
        const constructiveOverlayType: ConstructiveOverlayType = {
            kind: "updateWorkspaceBoard",
            workspaceBoard,
        };
        await openConstructiveOverlay(constructiveOverlayType);
    }

    async function archiveBoard() {
        await openDestructiveOverlay({ kind: "archiveBoard", workspaceBoard });
        await archiveWorkspaceBoard(workspaceBoard);
    }
</script>

<Layout>
    <ContextMenuButton
        kind={{
            kind: "button",
            action: editBoard,
        }}
        label={$_("workspace-board-overlay.edit-board")}
        state="normal"
        icon={Pencil}
    />
    <ContextMenuButton
        kind={{
            kind: "button",
            action: archiveBoard,
        }}
        label={$_("workspace-board-overlay.archive-board")}
        state="normal"
        icon={Archive}
    />
</Layout>
