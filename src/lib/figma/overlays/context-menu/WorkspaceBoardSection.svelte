<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023, 2024 JWP Consulting GK

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
<script lang="ts">
    import {
        ArrowDown,
        ArrowUp,
        Pencil,
        Selector,
        Trash,
        X,
    } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import {
        moveWorkspaceBoardSection,
        deleteWorkspaceBoardSection as repoDeleteWorkspaceBoardSection,
    } from "$lib/repository/workspace/workspaceBoardSection";
    import {
        toggleWorkspaceBoardSectionOpen,
        workspaceBoardSectionClosed,
    } from "$lib/stores/dashboard";
    import {
        openConstructiveOverlay,
        openDestructiveOverlay,
    } from "$lib/stores/globalUi";
    import type {
        WorkspaceBoard,
        WorkspaceBoardSection,
    } from "$lib/types/workspace";

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
            (s: WorkspaceBoardSection) => s.uuid == workspaceBoardSection.uuid,
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
            { fetch },
        );
    }
    async function switchWithNextSection() {
        if (!nextSection) {
            throw new Error("Expected nextSection");
        }
        await moveWorkspaceBoardSection(
            workspaceBoardSection,
            nextSection._order,
            { fetch },
        );
    }

    async function updateWorkspaceBoardSection() {
        await openConstructiveOverlay({
            kind: "updateWorkspaceBoardSection",
            workspaceBoardSection,
        });
    }

    async function deleteWorkspaceBoardSection() {
        await openDestructiveOverlay({
            kind: "deleteWorkspaceBoardSection",
            workspaceBoardSection,
        });
        await repoDeleteWorkspaceBoardSection(workspaceBoardSection, {
            fetch,
        });
    }
</script>

<Layout>
    <ContextMenuButton
        kind={{
            kind: "button",
            action: toggleWorkspaceBoardSectionOpen.bind(
                null,
                workspaceBoardSection.uuid,
            ),
        }}
        label={closed
            ? $_("overlay.context-menu.workspace-board-section.expand-section")
            : $_(
                  "overlay.context-menu.workspace-board-section.collapse-section",
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
                "overlay.context-menu.workspace-board-section.switch-previous",
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
                "overlay.context-menu.workspace-board-section.switch-next",
            )}
            state="normal"
            icon={ArrowDown}
        />
    {/if}
    <ContextMenuButton
        kind={{
            kind: "button",
            action: updateWorkspaceBoardSection,
        }}
        label={$_("overlay.context-menu.workspace-board-section.edit-title")}
        state="normal"
        icon={Pencil}
    />
    <ContextMenuButton
        kind={{
            kind: "button",
            action: deleteWorkspaceBoardSection,
        }}
        label={$_(
            "overlay.context-menu.workspace-board-section.delete-workspace-board-section",
        )}
        state="normal"
        icon={Trash}
        color="destructive"
    />
</Layout>
