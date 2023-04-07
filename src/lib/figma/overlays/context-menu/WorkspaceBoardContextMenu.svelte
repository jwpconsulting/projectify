<script lang="ts">
    import { _ } from "svelte-i18n";
    import { Archive, Pencil } from "@steeze-ui/heroicons";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import type { WorkspaceBoard } from "$lib/types/workspace";

    export let workspaceBoard: WorkspaceBoard;

    // TODO
    console.log(workspaceBoard);
</script>

<ContextMenuButton
    kind={{
        kind: "button",
        action: () => console.error("edit board not implemented"),
    }}
    label={$_("workspace-board-overlay.edit-board")}
    state="normal"
    icon={Pencil}
/>
<ContextMenuButton
    kind={{
        kind: "button",
        action: () => console.error("archive board not implemented"),
    }}
    label={$_("workspace-board-overlay.archive-board")}
    state="normal"
    icon={Archive}
/>
