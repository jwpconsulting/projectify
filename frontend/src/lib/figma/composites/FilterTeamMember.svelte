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
    import { Search } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { _ } from "svelte-i18n";

    import FilterUser from "$lib/figma/select-controls/FilterUser.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { tasksPerUser } from "$lib/stores/dashboard";
    import {
        filterByTeamMember,
        selectedTeamMember,
        unfilterByTeamMember,
        teamMemberSearch,
        teamMemberSearchResults,
    } from "$lib/stores/dashboard/teamMemberFilter";
    import type { TeamMemberAssignment } from "$lib/types/stores";
    import type {
        TeamMemberAssignmentState,
        TeamMemberSelection,
    } from "$lib/types/ui";
    import type { TeamMember } from "$lib/types/workspace";

    type FilterTeamMemberMenuMode =
        | { kind: "filter" }
        | { kind: "assign"; teamMemberAssignment: TeamMemberAssignment };

    export let mode: FilterTeamMemberMenuMode;

    $: selected =
        mode.kind === "filter"
            ? selectedTeamMember
            : mode.teamMemberAssignment.selected;
    $: select =
        mode.kind === "filter"
            ? filterByTeamMember
            : mode.teamMemberAssignment.select;
    $: deselect =
        mode.kind === "filter"
            ? unfilterByTeamMember
            : mode.teamMemberAssignment.deselect;

    function isSelected(
        $selected: TeamMemberAssignmentState | TeamMemberSelection,
        teamMember: TeamMember,
    ): boolean {
        if ($selected.kind === "teamMembers") {
            return $selected.teamMemberUuids.has(teamMember.uuid);
        } else if ($selected.kind === "teamMember") {
            return teamMember.uuid === $selected.teamMember.uuid;
        }
        return false;
    }
</script>

<!-- TODO remove px/pt here -->
<div class="flex flex-col px-4 pt-2">
    <InputField
        bind:value={$teamMemberSearch}
        style={{ inputType: "text" }}
        label={$_("dashboard.filter-team-members")}
        name="team-member-name"
        placeholder={$_("dashboard.team-member-name")}
    >
        <Icon
            slot="left"
            src={Search}
            class="w-4"
            theme="outline"
        /></InputField
    >
</div>
<div class="flex flex-col">
    <FilterUser
        teamMemberSelectionInput={{ kind: "unassigned" }}
        active={$selected.kind === "unassigned"}
        count={$tasksPerUser.unassigned}
        onSelect={() => select({ kind: "unassigned" })}
        onDeselect={() => deselect({ kind: "unassigned" })}
    />
    {#each $teamMemberSearchResults as teamMember (teamMember.uuid)}
        <FilterUser
            teamMemberSelectionInput={{
                kind: "teamMember",
                teamMember: teamMember,
            }}
            active={isSelected($selected, teamMember)}
            count={$tasksPerUser.assigned.get(teamMember.uuid)}
            onSelect={() =>
                select({
                    kind: "teamMember",
                    teamMember: teamMember,
                })}
            onDeselect={() =>
                deselect({
                    kind: "teamMember",
                    teamMember: teamMember,
                })}
        />
    {/each}
</div>
