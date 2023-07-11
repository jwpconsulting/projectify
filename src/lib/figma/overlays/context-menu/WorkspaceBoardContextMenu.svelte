<script lang="ts">
    import { _ } from "svelte-i18n";
    import { Archive, Pencil } from "@steeze-ui/heroicons";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import type { WorkspaceBoard } from "$lib/types/workspace";
    import type { ConstructiveOverlayType } from "$lib/types/ui";
    import { openConstructiveOverlay } from "$lib/stores/globalUi";

    export let workspaceBoard: WorkspaceBoard;

    // TODO
    function editBoard() {
        // open constructive dialog
        const constructiveOverlayType: ConstructiveOverlayType = {
            kind: "updateWorkspaceBoard",
            workspaceBoard,
        };
        const action = {
            kind: "sync" as const,
            action: console.error.bind(null, "Don't call me"),
        };
        openConstructiveOverlay(constructiveOverlayType, action);
    }

    function archiveBoard() {
        // open archive dialog
    }
</script>

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
