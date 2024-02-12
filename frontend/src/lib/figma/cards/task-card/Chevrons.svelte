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
<!--
@component
Up and down chevrons for task movement within a workspace board section
-->
<script lang="ts">
    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import { getTaskPosition, moveUp, moveDown } from "$lib/stores/modules";
    import type {
        Task,
        WorkspaceBoardSectionWithTasks,
    } from "$lib/types/workspace";

    export let task: Task;
    export let workspaceBoardSection: WorkspaceBoardSectionWithTasks;

    let upDisabled = true;
    let downDisabled = true;
    $: {
        const position = getTaskPosition(workspaceBoardSection, task);
        upDisabled = position.kind === "start";
        // If we are the only task, we don't want to show the down chevron.
        downDisabled =
            position.kind === "start"
                ? position.isOnly
                : position.kind === "end";
    }
</script>

<div class="flex flex-row items-center gap-1">
    <CircleIcon
        size="medium"
        icon="up"
        action={{
            kind: "button",
            action: () => moveUp(workspaceBoardSection, task, { fetch }),
            disabled: upDisabled,
        }}
    />
    <CircleIcon
        size="medium"
        icon="down"
        action={{
            kind: "button",
            action: () => moveDown(workspaceBoardSection, task, { fetch }),
            disabled: downDisabled,
        }}
    />
</div>
