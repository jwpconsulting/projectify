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
    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import { updateTask } from "$lib/repository/workspace";
    import { createWorkspaceUserAssignment } from "$lib/stores/dashboard/workspaceUserAssignment";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { ContextMenuType } from "$lib/types/ui";
    import type { TaskWithWorkspaceBoardSection } from "$lib/types/workspace";

    export let task: TaskWithWorkspaceBoardSection;

    let userPickerBtnRef: HTMLElement;

    $: workspaceUserAssignment = createWorkspaceUserAssignment(task);

    $: assignee = task.assignee ?? $workspaceUserAssignment;

    async function openUserPicker() {
        const contextMenuType: ContextMenuType = {
            kind: "updateWorkspaceUser",
            workspaceUserAssignment,
        };
        await openContextMenu(contextMenuType, userPickerBtnRef);
        const workspaceUser = $workspaceUserAssignment;
        // XXX need to investigate what happens when sub tasks change while
        // the user picker is open. Possibly, a sub task can be deleted if
        // it is added
        await updateTask(
            task,
            { ...task, assignee: workspaceUser },
            {
                fetch,
            },
        );
    }
</script>

<button bind:this={userPickerBtnRef} on:click|preventDefault={openUserPicker}>
    <AvatarVariant
        content={{ kind: "single", user: assignee?.user }}
        size="small"
    />
</button>
