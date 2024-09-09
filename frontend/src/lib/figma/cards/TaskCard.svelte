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
    import { _ } from "svelte-i18n";
    import Chevrons from "$lib/figma/cards/task-card/Chevrons.svelte";
    import Labels from "$lib/figma/cards/task-card/Labels.svelte";
    import MenuButton from "$lib/figma/cards/task-card/MenuButton.svelte";
    import SubTaskProgress from "$lib/figma/cards/task-card/SubTaskProgress.svelte";
    import TeamMember from "$lib/figma/cards/task-card/TeamMember.svelte";
    import { getTaskUrl } from "$lib/urls";
    import { currentSectionTask } from "$lib/stores/dashboard/ui";
    import type {
        ProjectDetail,
        ProjectDetailTask,
        ProjectDetailSection,
    } from "$lib/types/workspace";

    export let task: ProjectDetailTask;
    export let project: ProjectDetail;
    export let section: ProjectDetailSection | undefined = undefined;

    let anchor: HTMLElement | undefined;
    let taskSelected = false;

    $: {
        taskSelected = $currentSectionTask?.taskUuid === task.uuid;
        if (taskSelected && anchor) {
            anchor.focus();
        }
    }
</script>

<tr
    class="flex w-full flex-col items-center gap-1 rounded-lg border border-border p-3 lg:contents"
    class:ring={taskSelected}
>
    <td class="contents">
        <a
            bind:this={anchor}
            href={getTaskUrl(task)}
            class="flex flex-row items-start items-center gap-1 self-start sm:gap-6 lg:self-center {taskSelected
                ? 'lg:ring'
                : ''}"
        >
            <span class="shrink-0 font-bold"
                >{$_("dashboard.task-card.task-number", {
                    values: { number: task.number },
                })}</span
            >
            <span
                class="line-clamp-3 justify-self-start hover:text-primary lg:line-clamp-1 lg:h-6"
                >{task.title}</span
            >
        </a>
    </td>
    <td class="contents">
        <Labels {task} />
    </td>
    <td class="flex flex-row items-center justify-end gap-2 self-end">
        <SubTaskProgress {task} />
        <div class="flex flex-row items-center gap-2">
            <TeamMember {task} />
            <div class="flex flex-row items-center">
                {#if section}
                    <Chevrons {task} {section} />
                {/if}
                <MenuButton {task} {project} {section} />
            </div>
        </div>
    </td>
</tr>
