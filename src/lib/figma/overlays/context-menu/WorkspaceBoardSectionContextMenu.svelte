<script lang="ts">
    import { _ } from "svelte-i18n";
    import {
        ArrowDown,
        ArrowUp,
        Pencil,
        Plus,
        Selector,
        Trash,
        X,
    } from "@steeze-ui/heroicons";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import type { WorkspaceBoardSection } from "$lib/types/workspace";
    // TODO make injectable
    import type { WorkspaceBoardSectionModule } from "$lib/types/stores";

    export let workspaceBoardSection: WorkspaceBoardSection;
    export let workspaceBoardSectionModule: WorkspaceBoardSectionModule;

    let {
        workspaceBoardSectionClosed,
        toggleWorkspaceBoardSectionOpen,
        switchWithPrevSection,
        switchWithNextSection,
    } = workspaceBoardSectionModule;

    let closed: boolean;
    $: {
        closed = $workspaceBoardSectionClosed.has(workspaceBoardSection.uuid);
    }

    // TODO this might have to be refactored to check if previous or next section exists
</script>

<ContextMenuButton
    kind={{
        kind: "button",
        action: () =>
            toggleWorkspaceBoardSectionOpen(workspaceBoardSection.uuid),
    }}
    label={closed
        ? $_("workspace-board-section-overlay.expand-section")
        : $_("workspace-board-section-overlay.collapse-section")}
    state="normal"
    icon={closed ? Selector : X}
/>
<ContextMenuButton
    kind={{
        kind: "button",
        action: switchWithPrevSection.bind(null, workspaceBoardSection),
    }}
    label={$_("workspace-board-section-overlay.switch-previous")}
    state="normal"
    icon={ArrowUp}
/>
<ContextMenuButton
    kind={{
        kind: "button",
        action: switchWithNextSection.bind(null, workspaceBoardSection),
    }}
    label={$_("workspace-board-section-overlay.switch-next")}
    state="normal"
    icon={ArrowDown}
/>
<ContextMenuButton
    kind={{
        kind: "button",
        action: () => console.error("edit section title not implemented"),
    }}
    label={$_("workspace-board-section-overlay.edit-title")}
    state="normal"
    icon={Pencil}
/>
<ContextMenuButton
    kind={{
        kind: "button",
        action: () => console.error("add task not implemented"),
    }}
    label={$_("workspace-board-section-overlay.add-task")}
    state="normal"
    icon={Plus}
/>
<ContextMenuButton
    kind={{
        kind: "button",
        action: () => console.error("delete section not implemented"),
    }}
    label={$_("workspace-board-section-overlay.delete-section")}
    state="normal"
    icon={Trash}
    color="destructive"
/>
