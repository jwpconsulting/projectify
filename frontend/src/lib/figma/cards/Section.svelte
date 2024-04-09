<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023-2024 JWP Consulting GK

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

    import SectionTitle from "$lib/figma/cards/section-bar/SectionTitle.svelte";
    import TaskCard from "$lib/figma/cards/TaskCard.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { sectionClosed } from "$lib/stores/dashboard";
    import type {
        ProjectDetail,
        SectionWithTasks,
    } from "$lib/types/workspace";
    import { getNewTaskUrl } from "$lib/urls";

    export let project: ProjectDetail;
    export let section: SectionWithTasks;

    const { uuid } = section;
    $: open = !$sectionClosed.has(uuid);
</script>

<section class="flex flex-col">
    <SectionTitle {project} {section} {open} />
    {#if open}
        <div class="flex flex-col gap-2 rounded-b-2xl bg-foreground p-4">
            {#each section.tasks as task (task.uuid)}
                <TaskCard
                    {project}
{task}
                    {section}
                />
            {:else}
                <p>
                    {$_("dashboard.section.empty.message")}
                    <Anchor
                        label={$_("dashboard.section.empty.prompt")}
                        size="normal"
                        href={getNewTaskUrl(section.uuid)}
                    />
                </p>
            {/each}
        </div>
    {/if}
</section>
