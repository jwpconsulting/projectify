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
        TaskWithSection,
        ProjectDetail,
        SectionWithTasks,
    } from "$lib/types/workspace";

    export let task: TaskWithSection;
    export let project: ProjectDetail;
    export let section: SectionWithTasks | undefined = undefined;
</script>

<section class="w-full rounded-lg border border-base-300 bg-base-100 p-2">
    <!-- Compact view (< lg)-->
    <div class="flex flex-col lg:hidden">
        <div class="flex flex-row justify-between">
            <Title {task} />
            <div class="flex flex-row items-center gap-2 justify-self-end">
                {#if section}
                    <Chevrons {task} {section} />
                {/if}
                <MenuButton {task} {project} {section} />
            </div>
        </div>
        <div class="flex flex-row justify-between">
            <Labels {task} />
            <div class="flex shrink-0 flex-row justify-self-end">
                <div class="flex flex-row items-center gap-4">
                    <SubTaskProgress {task} />
                </div>
                <div class="flex flex-row items-center">
                    <TeamMember {task} />
                </div>
            </div>
        </div>
    </div>
    <!-- Wide view (lg) -->
    <div class="hidden w-full grid-cols-[8fr_5fr_4fr] items-center lg:grid">
        <Title {task} />
        <Labels {task} />
        <div class="flex flex-row items-center justify-end gap-2">
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
        </div>
    </div>
</section>
