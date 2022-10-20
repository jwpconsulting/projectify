<script lang="ts">
    import { _ } from "svelte-i18n";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import { Pencil, Archive } from "@steeze-ui/heroicons";
    import type { WorkspaceBoard } from "$lib/types/workspace";

    export let workspaceBoard: WorkspaceBoard;

    // TODO
    console.log(workspaceBoard);
</script>

<ContextMenuButton
    kind={{ kind: "button" }}
    on:click={() => console.error("edit board not implemented")}
    label={$_("workspace-board-overlay.edit-board")}
    state="normal"
    icon={Pencil}
/>
<ContextMenuButton
    kind={{ kind: "button" }}
    on:click={() => console.error("archive board not implemented")}
    label={$_("workspace-board-overlay.archive-board")}
    state="normal"
    icon={Archive}
/>
