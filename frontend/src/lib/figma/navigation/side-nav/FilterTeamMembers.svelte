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
    import { Plus, User } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import SideNavMenuCategory from "$lib/figma/buttons/SideNavMenuCategory.svelte";
    import FilterTeamMember from "$lib/figma/composites/FilterTeamMember.svelte";
    import {
        userExpandOpen,
        toggleUserExpandOpen,
    } from "$lib/stores/dashboard/ui";
    import { selectedTeamMember } from "$lib/stores/dashboard/teamMemberFilter";
    import { currentWorkspace } from "$lib/stores/dashboard/workspace";
    import { currentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import { getSettingsUrl } from "$lib/urls";
</script>

<SideNavMenuCategory
    label={$_("dashboard.side-nav.filter-team-members.title")}
    icon={User}
    open={$userExpandOpen}
    on:click={toggleUserExpandOpen}
    filtered={$selectedTeamMember.kind !== "allTeamMembers"}
/>
{#if $userExpandOpen}
    <!-- TODO evaluate removing this shrink class here -->
    <div class="shrink">
        <FilterTeamMember mode={{ kind: "filter" }} />
        {#if $currentWorkspace.value && $currentTeamMemberCan("create", "teamMemberInvite")}
            <ContextMenuButton
                kind={{
                    kind: "a",
                    href: getSettingsUrl(
                        $currentWorkspace.value,
                        "team-members",
                    ),
                }}
                icon={Plus}
                color="primary"
                label={$_("dashboard.side-nav.filter-team-members.add")}
            />
        {/if}
    </div>
{/if}
