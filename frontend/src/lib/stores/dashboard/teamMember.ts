// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
/*
 * Team member related store
 * Following use cases:
 *
 * - Selecting a user to be assigned to task (teamMemberAssignment)
 * - Filtering tasks inside a ws board by ws user
 * (teamMemberFilter)
 * Before I wrote these two things to be the same, even though that meant
 * unnecessarily shoehorning unrelated features into the same thing
 */
import { derived } from "svelte/store";
import type { Readable } from "svelte/store";

import { can, type Resource, type Verb } from "$lib/rules/workspace";
import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import type { Workspace, TeamMember } from "$lib/types/workspace";

import { currentUser } from "../user";

// TODO make Readable<TeamMember[] | undefined>
export type CurrentTeamMembers = Readable<TeamMember[]>;

export const currentTeamMembers: CurrentTeamMembers = derived<
    typeof currentWorkspace,
    TeamMember[]
    // Derived stores are initialized with undefined
>(
    currentWorkspace,
    ($currentWorkspace: Workspace | undefined, set) => {
        if (!$currentWorkspace) {
            return;
        }
        if (!$currentWorkspace.team_members) {
            throw new Error("Expected $currentWorkspace.team_members");
        }
        set($currentWorkspace.team_members);
    },
    [],
);

type CurrentTeamMember = Readable<TeamMember | undefined>;

/**
 * Find current team member belonging to logged in user
 */
export const currentTeamMember: CurrentTeamMember = derived<
    [typeof currentUser, typeof currentWorkspace],
    TeamMember | undefined
>(
    [currentUser, currentWorkspace],
    ([$user, $currentWorkspace], set) => {
        if ($user === undefined || $currentWorkspace === undefined) {
            set(undefined);
            return;
        }
        const wsUser = $currentWorkspace.team_members.find(
            (wsUser) => wsUser.user.email === $user.email,
        );
        if (wsUser === undefined) {
            throw new Error("Couldn't find currentTeamMember");
        }
        set(wsUser);
    },
    undefined,
);

type CurrentTeamMemberCan = Readable<
    (verb: Verb, resource: Resource) => boolean
>;

/**
 * A store that returns a function that allows permission checking for the
 * currently active, logged in user's team member.
 */
export const currentTeamMemberCan: CurrentTeamMemberCan = derived<
    [CurrentTeamMember, typeof currentWorkspace],
    (verb: Verb, resource: Resource) => boolean
>(
    [currentTeamMember, currentWorkspace],
    ([$currentTeamMember, $currentWorkspace], set) => {
        if ($currentTeamMember === undefined) {
            console.warn("teamMember was undefined");
            set(() => false);
            return;
        }
        if ($currentWorkspace === undefined) {
            console.warn("workspace was undefined");
            set(() => false);
            return;
        }
        const fn = (verb: Verb, resource: Resource) =>
            can(
                verb,
                resource,
                $currentTeamMember,
                $currentWorkspace.quota,
            );
        set(fn);
    },
    () => false,
);
