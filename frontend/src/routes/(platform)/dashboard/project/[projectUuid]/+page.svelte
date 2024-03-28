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

    import Loading from "$lib/components/loading.svelte";
    import SectionC from "$lib/figma/cards/Section.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { currentProject, currentSections } from "$lib/stores/dashboard";
    import { currentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import { openConstructiveOverlay } from "$lib/stores/globalUi";
    import type { SectionWithTasks } from "$lib/types/workspace";

    $: project = $currentProject;

    $: hasSections = project ? project.sections.length > 0 : false;

    let sections: SectionWithTasks[];
    $: sections = $currentSections ?? [];

    async function onAddNewSection() {
        if (!project) {
            throw new Error("Expected project");
        }
        await openConstructiveOverlay({
            kind: "createSection",
            project,
        });
    }
</script>

<svelte:head>
    {#if project}
        <title
            >{$_("dashboard.title", {
                values: { title: project.title },
            })}</title
        >
    {/if}
</svelte:head>

<!-- Sections -->
<div class="flex flex-col gap-4 md:p-2">
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
</div>

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
