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
    import type {
        WorkspaceBoard,
        WorkspaceBoardSection,
    } from "$lib/types/workspace";
    // TODO make injectable
    import {
        toggleWorkspaceBoardSectionOpen,
        workspaceBoardSectionClosed,
    } from "$lib/stores/dashboard";
    import { moveWorkspaceBoardSection } from "$lib/repository/workspace";

    export let workspaceBoard: WorkspaceBoard;
    export let workspaceBoardSection: WorkspaceBoardSection;

    let closed: boolean;
    $: {
        closed = $workspaceBoardSectionClosed.has(workspaceBoardSection.uuid);
    }

    let workspaceBoardSections: WorkspaceBoardSection[] = [];
    $: workspaceBoardSections = workspaceBoard.workspace_board_sections ?? [];

    // TODO this might have to be refactored to check if previous or next section exists

    let sectionIndex: number | undefined;
    let previousIndex: number | undefined;
    let nextIndex: number | undefined;
    let previousSection: WorkspaceBoardSection | undefined;
    let nextSection: WorkspaceBoardSection | undefined;

    $: {
        sectionIndex = workspaceBoardSections.findIndex(
            (s: WorkspaceBoardSection) => s.uuid == workspaceBoardSection.uuid
        );
        previousIndex = sectionIndex > 0 ? sectionIndex - 1 : undefined;
        nextIndex =
            sectionIndex < workspaceBoardSections.length - 1
                ? sectionIndex + 1
                : undefined;
        previousSection =
            previousIndex !== undefined
                ? workspaceBoardSections[previousIndex]
                : undefined;
        nextSection =
            nextIndex !== undefined
                ? workspaceBoardSections[nextIndex]
                : undefined;
    }

    async function switchWithPreviousSection() {
        if (!previousSection) {
            throw new Error("Expected previousSection");
        }
        await moveWorkspaceBoardSection(
            workspaceBoardSection,
            previousSection._order
        );
    }
    async function switchWithNextSection() {
        if (!nextSection) {
            throw new Error("Expected nextSection");
        }
        await moveWorkspaceBoardSection(
            workspaceBoardSection,
            nextSection._order
        );
    }
</script>

<ContextMenuButton
    kind={{
        kind: "button",
        action: toggleWorkspaceBoardSectionOpen.bind(
            null,
            workspaceBoardSection.uuid
        ),
    }}
    label={closed
        ? $_("workspace-board-section-overlay.expand-section")
        : $_("workspace-board-section-overlay.collapse-section")}
    state="normal"
    icon={closed ? Selector : X}
/>
{#if previousSection}
    <ContextMenuButton
        kind={{
            kind: "button",
            action: switchWithPreviousSection,
        }}
        label={$_("workspace-board-section-overlay.switch-previous")}
        state="normal"
        icon={ArrowUp}
    />
{/if}
{#if nextSection}
    <ContextMenuButton
        kind={{
            kind: "button",
            action: switchWithNextSection,
        }}
        label={$_("workspace-board-section-overlay.switch-next")}
        state="normal"
        icon={ArrowDown}
    />
{/if}
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
