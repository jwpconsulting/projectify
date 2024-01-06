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
    import SideNav from "$lib/figma/navigation/SideNav.svelte";
    import {
        currentWorkspace,
        currentWorkspaces,
    } from "$lib/stores/dashboard";
    import type { Workspace } from "$lib/types/workspace";

    let workspace: Workspace | undefined = undefined;
    let workspaces: Workspace[] = [];

    $: workspaces = $currentWorkspaces ?? [];
    $: workspace = $currentWorkspace;
</script>

<div class="flex min-h-0 shrink grow flex-row">
    <!-- this breakpoint is in tune with the mobile menu breakpoint -->
    <div class="hidden h-full shrink-0 overflow-y-auto md:block">
        {#if workspace}
            <SideNav {workspaces} {workspace} />
        {:else}
            Loading workspaces
        {/if}
    </div>
    <!-- not inserting min-w-0 will mean that this div will extend as much as
    needed around whatever is inside the slot -->
    <div class="min-w-0 grow overflow-y-auto">
        <slot />
    </div>
</div>
