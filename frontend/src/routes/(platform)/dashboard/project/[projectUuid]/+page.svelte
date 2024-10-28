<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import SectionC from "$lib/figma/cards/Section.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { currentProject } from "$lib/stores/dashboard/project";
    import { currentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import { openConstructiveOverlay } from "$lib/stores/globalUi";
    import type { ProjectDetailSection } from "$lib/types/workspace";
    import { currentSections } from "$lib/stores/dashboard/section";
    import { handleKey } from "$lib/utils/keyboard";
    import { onMount } from "svelte";
    import { selectInProject } from "$lib/stores/dashboard/ui";
    import type { PageData } from "./$types";

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
    <SectionC {project} {section} />
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
