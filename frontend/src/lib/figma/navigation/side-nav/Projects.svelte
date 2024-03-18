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
    import { Folder, Plus } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import Loading from "$lib/components/loading.svelte";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import SideNavMenuCategory from "$lib/figma/buttons/SideNavMenuCategory.svelte";
    import SelectProject from "$lib/figma/navigation/side-nav/SelectProject.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { currentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import {
        projectExpandOpen,
        toggleProjectExpandOpen,
    } from "$lib/stores/dashboard/ui";
    import { openConstructiveOverlay } from "$lib/stores/globalUi";
    import type { Workspace } from "$lib/types/workspace";
    import { getArchiveUrl } from "$lib/urls";

    export let workspace: Workspace;

    async function openCreateProject() {
        const target = {
            kind: "createProject" as const,
            workspace,
        };
        await openConstructiveOverlay(target);
    }
</script>

<SideNavMenuCategory
    label={$_("dashboard.projects")}
    icon={Folder}
    open={$projectExpandOpen}
    on:click={toggleProjectExpandOpen}
    filtered={false}
/>
{#if $projectExpandOpen}
    <div class="flex shrink flex-col overflow-y-auto">
        {#if workspace.projects === undefined}
            <Loading />
        {:else if workspace.projects.length === 0}
            <div class="flex flex-col gap-2 p-4">
                <p>
                    {$_("dashboard.side-nav.projects.empty.message")}
                </p>
                <p>
                    <Anchor
                        label={$_("dashboard.side-nav.projects.empty.archive")}
                        href={getArchiveUrl(workspace.uuid)}
                        size="normal"
                    />
                </p>
            </div>
        {:else}
            {#each workspace.projects as project (project.uuid)}
                <SelectProject {workspace} {project} />
            {/each}
        {/if}
    </div>
    {#if $currentTeamMemberCan("create", "project")}
        <ContextMenuButton
            label={$_("dashboard.create-project")}
            icon={Plus}
            color="primary"
            state="normal"
            kind={{ kind: "button", action: openCreateProject }}
        />
    {/if}
{/if}
