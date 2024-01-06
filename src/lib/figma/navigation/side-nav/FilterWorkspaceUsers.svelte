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
    import { User } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import SideNavMenuCategory from "$lib/figma/buttons/SideNavMenuCategory.svelte";
    import FilterWorkspaceUser from "$lib/figma/composites/FilterWorkspaceUser.svelte";
    import {
        userExpandOpen,
        toggleUserExpandOpen,
    } from "$lib/stores/dashboard";
    import { selectedWorkspaceUser } from "$lib/stores/dashboard/workspaceUserFilter";
</script>

<SideNavMenuCategory
    label={$_("dashboard.workspace-users")}
    icon={User}
    open={$userExpandOpen}
    on:click={toggleUserExpandOpen}
    filtered={$selectedWorkspaceUser.kind !== "allWorkspaceUsers"}
/>
{#if $userExpandOpen}
    <div class="shrink overflow-y-auto">
        <FilterWorkspaceUser mode={{ kind: "filter" }} />
    </div>
{/if}
