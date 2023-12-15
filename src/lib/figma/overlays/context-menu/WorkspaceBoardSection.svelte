<script lang="ts">
    import {
        ArrowDown,
        ArrowUp,
        Pencil,
        Plus,
        Selector,
        Trash,
        X,
    } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import { moveWorkspaceBoardSection } from "$lib/repository/workspace";
    import {
        toggleWorkspaceBoardSectionOpen,
        workspaceBoardSectionClosed,
    } from "$lib/stores/dashboard";
    import type {
        WorkspaceBoard,
        WorkspaceBoardSection,
    } from "$lib/types/workspace";
    import { getNewTaskUrl } from "$lib/urls";

    // TODO make injectable

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
            previousSection._order,
            { fetch }
        );
    }
    async function switchWithNextSection() {
        if (!nextSection) {
            throw new Error("Expected nextSection");
        }
        await moveWorkspaceBoardSection(
            workspaceBoardSection,
            nextSection._order,
            { fetch }
        );
    }
</script>

<Layout>
    <ContextMenuButton
        kind={{
            kind: "button",
            action: toggleWorkspaceBoardSectionOpen.bind(
                null,
                workspaceBoardSection.uuid
            ),
        }}
        label={closed
            ? $_("overlay.context-menu.workspace-board-section.expand-section")
            : $_(
                  "overlay.context-menu.workspace-board-section.collapse-section"
              )}
        state="normal"
        icon={closed ? Selector : X}
    />
    {#if previousSection}
        <ContextMenuButton
            kind={{
                kind: "button",
                action: switchWithPreviousSection,
            }}
            label={$_(
                "overlay.context-menu.workspace-board-section.switch-previous"
            )}
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
            label={$_(
                "overlay.context-menu.workspace-board-section.switch-next"
            )}
            state="normal"
            icon={ArrowDown}
        />
    {/if}
    <ContextMenuButton
        kind={{
            kind: "button",
            action: () => console.error("edit section title not implemented"),
        }}
        label={$_("overlay.context-menu.workspace-board-section.edit-title")}
        state="normal"
        icon={Pencil}
    />
    <ContextMenuButton
        kind={{
            kind: "a",
            href: getNewTaskUrl(workspaceBoardSection.uuid),
        }}
        label={$_("overlay.context-menu.workspace-board-section.add-task")}
        state="normal"
        icon={Plus}
    />
    <ContextMenuButton
        kind={{
            kind: "button",
            action: () => console.error("delete section not implemented"),
        }}
        label={$_(
            "overlay.context-menu.workspace-board-section.delete-workspace-board-section"
        )}
        state="normal"
        icon={Trash}
        color="destructive"
    />
</Layout>
