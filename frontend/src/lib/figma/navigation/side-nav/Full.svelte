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
    import { _ } from "svelte-i18n";

    import FilterLabels from "$lib/figma/navigation/side-nav/FilterLabels.svelte";
    import FilterWorkspaceUsers from "$lib/figma/navigation/side-nav/FilterWorkspaceUsers.svelte";
    import WorkspaceBoards from "$lib/figma/navigation/side-nav/WorkspaceBoards.svelte";
    import WorkspaceSelector from "$lib/figma/navigation/side-nav/WorkspaceSelector.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { showFilters } from "$lib/stores/dashboard";
    import type { WorkspaceDetail } from "$lib/types/workspace";

    export let workspace: WorkspaceDetail | undefined;
</script>

<!-- XXX temporary fix to alleviate long side nav inside mobile menu -->
<nav class="flex flex-col py-4">
    <WorkspaceSelector {workspace} open={true} />
    {#if workspace}
        {#if workspace.quota.workspace_status === "trial"}
            <p class="px-4">
                <strong>
                    {$_("dashboard.side-nav.quota.status.trial.label")}
                </strong>
                <Anchor
                    label={$_("dashboard.side-nav.quota.status.trial.help")}
                    href="/help/billing"
                    size="normal"
                    openBlank
                />
            </p>
        {:else if workspace.quota.workspace_status === "inactive"}
            <p class="px-4">
                <strong>
                    {$_("dashboard.side-nav.quota.status.inactive.label")}
                </strong>
                <Anchor
                    label={$_("dashboard.side-nav.quota.status.inactive.help")}
                    href="/help/billing"
                    size="normal"
                    openBlank
                />
            </p>
        {/if}
        <div class="flex shrink flex-col overflow-auto">
            <WorkspaceBoards {workspace} />
            {#if $showFilters}
                <FilterWorkspaceUsers />
                <FilterLabels />
            {/if}
        </div>
    {:else}
        <div class="flex flex-col gap-4 px-4">
            <p class="font-bold">
                {$_("dashboard.side-nav.no-workspace.title")}
            </p>
            <p>
                {$_("dashboard.side-nav.no-workspace.message")}
            </p>
        </div>
    {/if}
</nav>
