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

    import FilterLabelsClosed from "$lib/figma/navigation/side-nav/FilterLabelsClosed.svelte";
    import FilterTeamMembersClosed from "$lib/figma/navigation/side-nav/FilterTeamMembersClosed.svelte";
    import WorkspaceSelector from "$lib/figma/navigation/side-nav/WorkspaceSelector.svelte";
    import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";
    import { selectProjectUuid, showFilters } from "$lib/stores/dashboard/ui";
    import { getDashboardProjectUrl } from "$lib/urls";
    import { currentWorkspace } from "$lib/stores/dashboard/workspace";

    $: workspace = $currentWorkspace.value ?? undefined;
</script>

<nav class="inline-flex h-full flex-col items-center gap-12 bg-foreground p-4">
    <div class="flex flex-col items-center justify-between">
        <div class="flex flex-col items-center gap-12">
            <div
                class="flex flex-col items-center gap-6 border-b border-border pb-12"
            >
                <WorkspaceSelector {workspace} open={false} />
                <div class="flex flex-col items-center gap-6">
                    <div class="flex flex-col items-center gap-4">
                        {#if workspace?.projects}
                            {#each workspace.projects as project}
                                <SquovalIcon
                                    ariaLabel={$_(
                                        "dashboard.side-nav.projects.open-project",
                                        { values: { title: project.title } },
                                    )}
                                    icon="board"
                                    state="active"
                                    action={{
                                        kind: "a",
                                        href: getDashboardProjectUrl(project),
                                        onInteract: selectProjectUuid.bind(
                                            null,
                                            workspace.uuid,
                                            project.uuid,
                                        ),
                                    }}
                                />
                            {/each}
                        {/if}
                    </div>
                </div>
            </div>
            {#if workspace !== undefined && $showFilters}
                <div class="flex flex-col gap-8">
                    <div class="flex flex-col items-center gap-6">
                        <FilterTeamMembersClosed />
                        <FilterLabelsClosed />
                    </div>
                </div>
            {/if}
        </div>
    </div>
</nav>
