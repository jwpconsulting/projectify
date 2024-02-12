<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

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
    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { ContextMenuType } from "$lib/types/ui";
    import type {
        TaskWithWorkspaceBoardSection,
        WorkspaceBoardDetail,
        WorkspaceBoardSectionWithTasks,
    } from "$lib/types/workspace";

    export let task: TaskWithWorkspaceBoardSection;
    // this is only ever needed for the dashboard, not when a task is part
    // of search results... time for another ADT?
    export let workspaceBoard: WorkspaceBoardDetail;
    export let workspaceBoardSection:
        | WorkspaceBoardSectionWithTasks
        | undefined = undefined;

    let dropDownMenuBtnRef: HTMLElement;

    async function openDropDownMenu() {
        const contextMenu: ContextMenuType =
            workspaceBoardSection === undefined
                ? {
                      kind: "task",
                      task,
                      location: "task",
                      workspaceBoardSection: task.workspace_board_section,
                  }
                : {
                      kind: "task" as const,
                      task,
                      location: "dashboard" as const,
                      workspaceBoardSection,
                      workspaceBoard,
                  };
        await openContextMenu(contextMenu, dropDownMenuBtnRef);
    }

    const action = { kind: "button" as const, action: openDropDownMenu };
</script>

<div bind:this={dropDownMenuBtnRef}>
    <CircleIcon icon="ellipsis" size="medium" {action} />
</div>
