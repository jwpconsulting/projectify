<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
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
    import { getDisplayName } from "$lib/types/user";
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
    {#if $userExpandOpen && $teamMemberSearchResults !== undefined}
        <div class="flex flex-col items-center gap-2">
            <SelectTeamMemberClosed
                ariaLabel={$_("filter-team-member.assigned-nobody")}
                user={undefined}
                active={$selectedTeamMember.kind === "unassigned"}
                on:select={() => filterByTeamMember({ kind: "unassigned" })}
                on:deselect={() =>
                    unfilterByTeamMember({ kind: "unassigned" })}
            />
            {#each $teamMemberSearchResults as teamMember}
                <SelectTeamMemberClosed
                    ariaLabel={getDisplayName(teamMember.user)}
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
