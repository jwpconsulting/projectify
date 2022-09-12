<script lang="ts">
    import { _ } from "svelte-i18n";
    import MenuButton from "$lib/figma/MenuButton.svelte";
    import {
        Selector,
        Pencil,
        X,
        ArrowUp,
        ArrowDown,
        Plus,
        Trash,
    } from "@steeze-ui/heroicons";
    import type { WorkspaceBoardSection } from "$lib/types";
    import {
        workspaceBoardSectionClosed,
        toggleWorkspaceBoardSectionOpen,
    } from "$lib/stores/dashboard";

    export let workspaceBoardSection: WorkspaceBoardSection;
    let closed: boolean;
    $: {
        closed = $workspaceBoardSectionClosed.has(workspaceBoardSection.uuid);
    }

    // TODO this might have to be refactored to check if previous or next section exists
</script>

<MenuButton
    kind={{ kind: "button" }}
    on:click={() =>
        toggleWorkspaceBoardSectionOpen(workspaceBoardSection.uuid)}
    label={closed
        ? $_("workspace-board-section-overlay.expand-section")
        : $_("workspace-board-section-overlay.collapse-section")}
    state="normal"
    icon={closed ? Selector : X}
/>
<MenuButton
    kind={{ kind: "button" }}
    on:click={() => console.error("switch with previous not implemented")}
    label={$_("workspace-board-section-overlay.switch-previous")}
    state="normal"
    icon={ArrowUp}
/>
<MenuButton
    kind={{ kind: "button" }}
    on:click={() => console.error("switch with next not implemented")}
    label={$_("workspace-board-section-overlay.switch-next")}
    state="normal"
    icon={ArrowDown}
/>
<MenuButton
    kind={{ kind: "button" }}
    on:click={() => console.error("edit section title not implemented")}
    label={$_("workspace-board-section-overlay.edit-title")}
    state="normal"
    icon={Pencil}
/>
<MenuButton
    kind={{ kind: "button" }}
    on:click={() => console.error("add task not implemented")}
    label={$_("workspace-board-section-overlay.add-task")}
    state="normal"
    icon={Plus}
/>
<MenuButton
    kind={{ kind: "button" }}
    on:click={() => console.error("delete section not implemented")}
    label={$_("workspace-board-section-overlay.delete-section")}
    state="normal"
    icon={Trash}
    color="destructive"
/>
