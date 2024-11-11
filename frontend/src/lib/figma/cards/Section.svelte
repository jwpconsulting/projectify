<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import SectionTitle from "$lib/figma/cards/section-bar/SectionTitle.svelte";
    import TaskCard from "$lib/figma/cards/TaskCard.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import {
        sectionClosed,
        currentSectionTask,
    } from "$lib/stores/dashboard/ui";
    import type {
        ProjectDetail,
        ProjectDetailSection,
    } from "$lib/types/workspace";
    import { getNewTaskUrl } from "$lib/urls";

    export let project: ProjectDetail;
    export let section: ProjectDetailSection;

    const { uuid } = section;
    $: open = !$sectionClosed.has(uuid);
    $: selected = $currentSectionTask?.sectionUuid === section.uuid;
</script>

<section class="flex flex-col" class:ring={selected}>
    <SectionTitle {project} {section} {open} />
    {#if open}
        <table
            class="flex flex-col gap-2 rounded-b-2xl bg-foreground p-4 lg:grid lg:grid-cols-[8fr_3fr_max-content] lg:gap-4"
        >
            <tbody class="contents">
                {#each section.tasks as task (task.uuid)}
                    <TaskCard {project} {task} {section} />
                {:else}
                    <p>
                        {$_("dashboard.section.empty.message")}
                        <Anchor
                            label={$_("dashboard.section.empty.prompt")}
                            size="normal"
                            href={getNewTaskUrl(section)}
                        />
                    </p>
                {/each}
            </tbody>
        </table>
    {/if}
</section>
