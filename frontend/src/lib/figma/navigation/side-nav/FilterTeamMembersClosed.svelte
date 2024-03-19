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

    import SelectTeamMemberClosed from "$lib/figma/navigation/side-nav/SelectTeamMemberClosed.svelte";
    import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";
    import {
        selectedTeamMember,
        filterByTeamMember,
        unfilterByTeamMember,
        teamMemberSearchResults,
    } from "$lib/stores/dashboard/teamMemberFilter";
    import {
        toggleUserExpandOpen,
        userExpandOpen,
    } from "$lib/stores/dashboard/ui";
</script>

<div class="flex flex-col items-center gap-6">
    <SquovalIcon
        ariaLabel={$userExpandOpen
            ? $_("dashboard.side-nav.filter-team-members.close-collapsible")
            : $_("dashboard.side-nav.filter-team-members.open-collapsible")}
        state="active"
        icon="teamMember"
        action={{ kind: "button", action: toggleUserExpandOpen }}
        active={$selectedTeamMember.kind === "teamMembers"}
    />
    {#if $userExpandOpen}
        <div class="flex flex-col items-center gap-2">
            <SelectTeamMemberClosed
                user={undefined}
                active={$selectedTeamMember.kind === "unassigned"}
                on:select={() => filterByTeamMember({ kind: "unassigned" })}
                on:deselect={() =>
                    unfilterByTeamMember({ kind: "unassigned" })}
            />
            {#each $teamMemberSearchResults as teamMember}
                <SelectTeamMemberClosed
                    user={teamMember.user}
                    active={$selectedTeamMember.kind === "teamMembers" &&
                        $selectedTeamMember.teamMemberUuids.has(
                            teamMember.uuid,
                        )}
                    on:select={() =>
                        filterByTeamMember({
                            kind: "teamMember",
                            teamMember,
                        })}
                    on:deselect={() =>
                        unfilterByTeamMember({
                            kind: "teamMember",
                            teamMember,
                        })}
                />
            {/each}
        </div>
    {/if}
</div>
