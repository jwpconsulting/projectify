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
        ArrowsExpand,
        ChevronDown,
        ChevronUp,
        Duplicate,
        SortAscending,
        SortDescending,
        SwitchVertical,
        Trash,
    } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import { goto } from "$lib/navigation";
    import { moveTaskToWorkspaceBoardSection } from "$lib/repository/workspace";
    import { deleteTask } from "$lib/stores/dashboard";
    import { openDestructiveOverlay } from "$lib/stores/globalUi";
    import {
        moveToTop,
        moveToBottom,
        getTaskPosition,
    } from "$lib/stores/modules";
    import type { ContextMenuType } from "$lib/types/ui";
    import type { WorkspaceBoardSection } from "$lib/types/workspace";
    import {
        getTaskUrl,
        getDashboardWorkspaceBoardSectionUrl,
    } from "$lib/urls";
    import { copyToClipboard } from "$lib/utils/clipboard";

    export let kind: ContextMenuType & { kind: "task" };

    async function promptDeleteTask() {
        const { uuid } = kind.workspaceBoardSection;
        await openDestructiveOverlay({
            kind: "deleteTask" as const,
            task: kind.task,
        });
        await deleteTask(kind.task);
        await goto(getDashboardWorkspaceBoardSectionUrl(uuid));
    }

    let moveToSectionOpened = false;

    function toggleMoveToSection() {
        moveToSectionOpened = !moveToSectionOpened;
    }

    async function moveToSection(section: WorkspaceBoardSection) {
        await moveTaskToWorkspaceBoardSection(kind.task, section, { fetch });
    }

    $: taskPosition =
        kind.location === "dashboard"
            ? getTaskPosition(kind.workspaceBoardSection, kind.task)
            : undefined;
    $: showMoveTop = taskPosition && taskPosition.kind !== "start";
    $: showMoveBottom =
        taskPosition &&
        (taskPosition.kind === "start"
            ? !taskPosition.isOnly
            : taskPosition.kind !== "end");
</script>

<Layout>
    {#if kind.location === "dashboard"}
        <ContextMenuButton
            kind={{
                kind: "a",
                href: getTaskUrl(kind.task.uuid),
            }}
            label={$_("overlay.context-menu.task.open-task")}
            state="normal"
            icon={ArrowsExpand}
        />
        <ContextMenuButton
            kind={{ kind: "button", action: toggleMoveToSection }}
            label={$_("overlay.context-menu.task.move-to-section")}
            state="normal"
            closeOnInteract={false}
            icon={SwitchVertical}
            iconRight={moveToSectionOpened ? ChevronUp : ChevronDown}
        />
        {#if moveToSectionOpened}
            {#each kind.workspaceBoard.workspace_board_sections as section}
                <ContextMenuButton
                    state="normal"
                    label={section.title}
                    kind={{
                        kind: "button",
                        action: moveToSection.bind(null, section),
                    }}
                />
            {/each}
        {/if}
        {#if showMoveTop}
            <ContextMenuButton
                kind={{
                    kind: "button",
                    action: moveToTop.bind(
                        null,
                        kind.workspaceBoardSection,
                        kind.task,
                        { fetch },
                    ),
                }}
                label={$_("overlay.context-menu.task.move-to-top")}
                state="normal"
                icon={SortAscending}
            />
        {/if}
        {#if showMoveBottom}
            <ContextMenuButton
                kind={{
                    kind: "button",
                    action: moveToBottom.bind(
                        null,
                        kind.workspaceBoardSection,
                        kind.task,
                        { fetch },
                    ),
                }}
                label={$_("overlay.context-menu.task.move-to-bottom")}
                state="normal"
                icon={SortDescending}
            />
        {/if}
    {/if}
    <ContextMenuButton
        kind={{
            kind: "button",
            action: copyToClipboard.bind(
                null,
                new URL(getTaskUrl(kind.task.uuid), document.baseURI).href,
            ),
        }}
        label={$_("overlay.context-menu.task.copy-link")}
        state="normal"
        icon={Duplicate}
    />
    <ContextMenuButton
        kind={{
            kind: "button",
            action: promptDeleteTask,
        }}
        label={$_("overlay.context-menu.task.delete-task")}
        state="normal"
        color="destructive"
        icon={Trash}
    />
</Layout>
