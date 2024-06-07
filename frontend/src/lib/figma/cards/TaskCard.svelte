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
    import Chevrons from "$lib/figma/cards/task-card/Chevrons.svelte";
    import Labels from "$lib/figma/cards/task-card/Labels.svelte";
    import MenuButton from "$lib/figma/cards/task-card/MenuButton.svelte";
    import SubTaskProgress from "$lib/figma/cards/task-card/SubTaskProgress.svelte";
    import TeamMember from "$lib/figma/cards/task-card/TeamMember.svelte";
    import Title from "$lib/figma/cards/task-card/Title.svelte";
    import type {
        ProjectDetail,
        ProjectDetailTask,
        SectionWithTasks,
    } from "$lib/types/workspace";

    export let task: ProjectDetailTask;
    export let project: ProjectDetail;
    export let section: SectionWithTasks | undefined = undefined;
</script>

<tr
    class="flex w-full flex-col items-center gap-1 rounded-lg border border-border p-3 lg:contents"
>
    <td class="contents">
        <Title {task} />
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
