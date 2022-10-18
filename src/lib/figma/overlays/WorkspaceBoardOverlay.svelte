<script lang="ts">
    import { _ } from "svelte-i18n";
    import MenuButton from "$lib/figma/buttons/MenuButton.svelte";
    import { Pencil, Archive } from "@steeze-ui/heroicons";
    import type { WorkspaceBoard } from "$lib/types/workspace";

    export let workspaceBoard: WorkspaceBoard;

    // TODO
    console.log(workspaceBoard);
</script>

<MenuButton
    kind={{ kind: "button" }}
    on:click={() => console.error("edit board not implemented")}
    label={$_("workspace-board-overlay.edit-board")}
    state="normal"
    icon={Pencil}
/>
<MenuButton
    kind={{ kind: "button" }}
    on:click={() => console.error("archive board not implemented")}
    label={$_("workspace-board-overlay.archive-board")}
    state="normal"
    icon={Archive}
/>
