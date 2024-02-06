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
    import Collapsed from "$lib/figma/navigation/side-nav/Collapsed.svelte";
    import Full from "$lib/figma/navigation/side-nav/Full.svelte";
    import { sideNavOpen } from "$lib/stores/dashboard";
    import type { Workspace } from "$lib/types/workspace";

    export let workspaces: Workspace[] | undefined;
    export let workspace: Workspace | undefined;
</script>

{#if $sideNavOpen}
    <div class="max-w-xs 2xl:max-w-md">
        <Full {workspaces} {workspace} />
    </div>
{:else}
    <!-- Figma says 72px but we only have 64 or 80 (16, 29 rem respectively)-->
    <!-- Might we refactor this into something separate? -->
    <div class="w-20">
        <Collapsed {workspace} {workspaces} />
    </div>
{/if}
