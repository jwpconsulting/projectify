<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { Search } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { _ } from "svelte-i18n";

    import FilterTeamMember from "$lib/figma/select-controls/FilterTeamMember.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { tasksPerUser } from "$lib/stores/dashboard/section";
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
    import type { ProjectDetailAssignee } from "$lib/types/workspace";
    import Loading from "$lib/components/Loading.svelte";

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
        teamMember: ProjectDetailAssignee,
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
        label={$_("dashboard.side-nav.filter-team-members.input.label")}
        name="team-member-name"
        placeholder={$_(
            "dashboard.side-nav.filter-team-members.input.placeholder",
        )}
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
    <FilterTeamMember
        teamMemberSelectionInput={{ kind: "unassigned" }}
        active={$selected.kind === "unassigned"}
        count={$tasksPerUser.unassigned}
        onSelect={() => select({ kind: "unassigned" })}
        onDeselect={() => deselect({ kind: "unassigned" })}
    />
    {#if $teamMemberSearchResults}
        {#each $teamMemberSearchResults as teamMember (teamMember.uuid)}
            <FilterTeamMember
                teamMemberSelectionInput={{
                    kind: "teamMember",
                    teamMember: teamMember,
                }}
                active={isSelected($selected, teamMember)}
                count={$tasksPerUser.assigned.get(teamMember.uuid) ?? 0}
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
    {:else}
        <Loading />
    {/if}
</div>
