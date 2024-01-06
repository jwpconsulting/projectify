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
    import Fields from "$lib/figma/screens/task/Fields.svelte";
    import TaskDescription from "$lib/figma/screens/task/TaskDescription.svelte";
    import TaskDueDate from "$lib/figma/screens/task/TaskDueDate.svelte";
    import TaskLabel from "$lib/figma/screens/task/TaskLabel.svelte";
    import TaskTitle from "$lib/figma/screens/task/TaskTitle.svelte";
    import TaskUser from "$lib/figma/screens/task/TaskUser.svelte";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type {
        LabelAssignment,
        WorkspaceUserAssignment,
    } from "$lib/types/stores";

    export let action: () => void;

    export let title: string | undefined;
    export let description: string | undefined;
    export let dueDate: string | undefined;

    export let workspaceUserAssignment: WorkspaceUserAssignment;
    export let labelAssignment: LabelAssignment;

    async function showUpdateWorkspaceUser(anchor: HTMLElement) {
        await openContextMenu(
            {
                kind: "updateWorkspaceUser",
                workspaceUserAssignment,
            },
            anchor,
        );
    }
    async function showUpdateLabel(anchor: HTMLElement) {
        await openContextMenu(
            {
                kind: "updateLabel",
                labelAssignment,
            },
            anchor,
        );
    }
</script>

<form on:submit|preventDefault={action} id="task-form">
    <input type="submit" class="hidden" />
    <Fields>
        <TaskTitle slot="title" bind:title />
        <TaskUser
            slot="assignee"
            onInteract={showUpdateWorkspaceUser}
            workspaceUser={$workspaceUserAssignment}
        />
        <TaskLabel
            slot="labels"
            onInteract={showUpdateLabel}
            labels={$labelAssignment ?? []}
        />
        <TaskDueDate slot="due-date" bind:dueDate />
        <TaskDescription slot="description" bind:description />
    </Fields>
</form>
