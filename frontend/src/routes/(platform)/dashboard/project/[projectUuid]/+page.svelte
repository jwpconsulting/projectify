<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import { getNewTaskUrl } from "$lib/urls";
    import SectionTitle from "$lib/figma/cards/section-bar/SectionTitle.svelte";
    import TaskCard from "$lib/figma/cards/TaskCard.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { currentProject } from "$lib/stores/dashboard/project";
    import {
        sectionClosed,
        currentSectionTask,
        selectInProject,
    } from "$lib/stores/dashboard/ui";
    import { openConstructiveOverlay } from "$lib/stores/globalUi";
    import type { ProjectDetailSection } from "$lib/types/workspace";
    import { currentSections } from "$lib/stores/dashboard/section";
    import { handleKey } from "$lib/utils/keyboard";
    import { onMount, getContext } from "svelte";
    import type { PageData } from "./$types";
    import type { CurrentTeamMemberCan } from "$lib/stores/dashboard/teamMember";

    const currentTeamMemberCan = getContext<CurrentTeamMemberCan>(
        "currentTeamMemberCan",
    );

    export let data: PageData;

    let { project } = data;
    $: project = $currentProject.or(data.project);

    $: hasSections = project.sections.length > 0;

    let sections: readonly ProjectDetailSection[];
    $: sections = $currentSections ?? [];

    async function onAddNewSection() {
        await openConstructiveOverlay({
            kind: "createSection",
            project,
        });
    }

    onMount(() => {
        return handleKey("j", () => selectInProject(project, "next-task"));
    });

    onMount(() => {
        return handleKey("k", () => selectInProject(project, "prev-task"));
    });

    onMount(() => {
        return handleKey("h", () => selectInProject(project, "prev-section"));
    });

    onMount(() => {
        return handleKey("l", () => selectInProject(project, "next-section"));
    });
</script>

<svelte:head>
    <title
        >{$_("dashboard.title", {
            values: { title: project.title },
        })}</title
    >
</svelte:head>

<!-- Sections -->
{#each sections as section (section.uuid)}
    {@const open = !$sectionClosed.has(section.uuid)}
    {@const isCurrentSection =
        $currentSectionTask?.sectionUuid === section.uuid}
    <section class="flex flex-col" class:ring={isCurrentSection}>
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
{:else}
    <section class="py-2 px-4 gap-8 bg-foreground rounded-lg flex flex-col">
        <p>
            {$_("dashboard.no-sections.message")}
        </p>
        <Button
            style={{ kind: "primary" }}
            color="blue"
            size="medium"
            grow={false}
            label={$_("dashboard.no-sections.prompt")}
            action={{ kind: "button", action: onAddNewSection }}
        />
    </section>
{/each}

{#if hasSections && $currentTeamMemberCan("create", "section")}
    <div class="sticky bottom-0 self-end p-2">
        <Button
            style={{ kind: "primary" }}
            label={$_("dashboard.actions.add-section")}
            size="medium"
            action={{ kind: "button", action: onAddNewSection }}
            color="blue"
        />
    </div>
{/if}
