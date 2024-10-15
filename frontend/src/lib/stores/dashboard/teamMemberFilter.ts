// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
/**
 * Filter used to filter tasks by team members
 */
import { derived, writable } from "svelte/store";
import type { Readable, Writable } from "svelte/store";

import { currentTeamMembers } from "$lib/stores/dashboard/teamMember";
import type { CurrentTeamMembers } from "$lib/stores/dashboard/teamMember";
import type { SearchInput } from "$lib/types/base";
import type {
    TeamMemberSelection,
    TeamMemberSelectionInput,
} from "$lib/types/ui";
import type { WorkspaceDetailTeamMember } from "$lib/types/workspace";

import { internallyWritable, searchAmong } from "../util";

const { priv: _selectedTeamMember, pub: selectedTeamMember } =
    internallyWritable<TeamMemberSelection>({
        kind: "allTeamMembers",
    });
export { selectedTeamMember };

type TeamMemberSearch = Writable<SearchInput>;
const createTeamMemberFilter = () => writable<SearchInput>(undefined);

function searchTeamMembers(
    teamMembers: readonly WorkspaceDetailTeamMember[],
    searchInput: SearchInput,
) {
    return searchAmong(
        ["user.email", "user.preferred_name"],
        teamMembers,
        searchInput,
    );
}

type TeamMemberSearchResults = Readable<
    readonly WorkspaceDetailTeamMember[] | undefined
>;

function createTeamMemberSearchResults(
    currentTeamMembers: CurrentTeamMembers,
    teamMemberSearch: TeamMemberSearch,
): TeamMemberSearchResults {
    return derived<
        [typeof currentTeamMembers, typeof teamMemberSearch],
        readonly WorkspaceDetailTeamMember[] | undefined
    >(
        [currentTeamMembers, teamMemberSearch],
        ([$currentTeamMembers, $teamMemberSearch], set) => {
            if (!$currentTeamMembers) {
                return;
            }
            set(searchTeamMembers($currentTeamMembers, $teamMemberSearch));
        },
        undefined,
    );
}

export const teamMemberSearch: TeamMemberSearch = createTeamMemberFilter();

export const teamMemberSearchResults: TeamMemberSearchResults =
    createTeamMemberSearchResults(currentTeamMembers, teamMemberSearch);

export function filterByTeamMember(selection: TeamMemberSelectionInput) {
    _selectedTeamMember.update(($selectedTeamMember: TeamMemberSelection) => {
        if (selection.kind === "allTeamMembers") {
            return { kind: "allTeamMembers" };
        } else if (selection.kind === "unassigned") {
            if ($selectedTeamMember.kind === "unassigned") {
                return { kind: "allTeamMembers" };
            } else {
                return { kind: "unassigned" };
            }
        } else {
            const selectionUuid = selection.teamMember.uuid;
            if ($selectedTeamMember.kind === "teamMembers") {
                $selectedTeamMember.teamMemberUuids.add(selectionUuid);
                return $selectedTeamMember;
            } else {
                const teamMemberUuids = new Set<string>();
                teamMemberUuids.add(selectionUuid);
                return { kind: "teamMembers", teamMemberUuids };
            }
        }
    });
}

export function unfilterByTeamMember(selection: TeamMemberSelectionInput) {
    _selectedTeamMember.update(($selectedTeamMember: TeamMemberSelection) => {
        if (selection.kind === "allTeamMembers") {
            return { kind: "allTeamMembers" };
        } else if (selection.kind === "unassigned") {
            if ($selectedTeamMember.kind === "unassigned") {
                return { kind: "allTeamMembers" };
            } else {
                return { kind: "unassigned" };
            }
        } else {
            const selectionUuid = selection.teamMember.uuid;
            if ($selectedTeamMember.kind === "teamMembers") {
                $selectedTeamMember.teamMemberUuids.delete(selectionUuid);
                if ($selectedTeamMember.teamMemberUuids.size === 0) {
                    return { kind: "allTeamMembers" };
                } else {
                    return $selectedTeamMember;
                }
            } else {
                return { kind: "allTeamMembers" };
            }
        }
    });
}
