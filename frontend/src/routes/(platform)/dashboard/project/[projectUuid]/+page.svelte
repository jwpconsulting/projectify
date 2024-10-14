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

    import Loading from "$lib/components/Loading.svelte";
    import SectionC from "$lib/figma/cards/Section.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { currentProject } from "$lib/stores/dashboard/project";
    import { currentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import { openConstructiveOverlay } from "$lib/stores/globalUi";
    import type {
        ProjectDetail,
        ProjectDetailSection,
    } from "$lib/types/workspace";
    import { currentSections } from "$lib/stores/dashboard/section";
    import { handleKey } from "$lib/utils/keyboard";
    import { onMount } from "svelte";
    import { selectInProject } from "$lib/stores/dashboard/ui";

    export let data: { injectProject?: ProjectDetail } | undefined = undefined;

    let project: ProjectDetail | undefined = undefined;
    $: project = $currentProject.value ?? data?.injectProject;

    $: hasSections = project ? project.sections.length > 0 : false;

    let sections: readonly ProjectDetailSection[];
    $: sections = $currentSections ?? data?.injectProject?.sections ?? [];

    async function onAddNewSection() {
        if (!project) {
            throw new Error("Expected project");
        }
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
    {#if project && data?.injectProject === undefined}<title
            >{$_("dashboard.title", {
                values: { title: project.title },
            })}</title
        >{/if}
</svelte:head>

<!-- Sections -->
{#if project}
    {#each sections as section (section.uuid)}
        <SectionC {project} {section} />
    {:else}
        <section
            class="py-2 px-4 gap-8 bg-foreground rounded-lg flex flex-col"
        >
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
{:else}
    <Loading />
{/if}

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
