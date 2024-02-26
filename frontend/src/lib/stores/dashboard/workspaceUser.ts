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
 * Workspace user related store
 * Following use cases:
 *
 * - Selecting a user to be assigned to task (workspaceUserAssignment)
 * - Filtering tasks inside a ws board by ws user
 * (workspaceUserFilter)
 * Before I wrote these two things to be the same, even though that meant
 * unnecessarily shoehorning unrelated features into the same thing
 */
import { derived } from "svelte/store";
import type { Readable } from "svelte/store";

import { can, type Resource, type Verb } from "$lib/rules/workspace";
import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import type { Workspace, WorkspaceUser } from "$lib/types/workspace";

import { currentUser } from "../user";

// TODO make Readable<WorkspaceUser[] | undefined>
export type CurrentWorkspaceUsers = Readable<WorkspaceUser[]>;

export const currentWorkspaceUsers: CurrentWorkspaceUsers = derived<
    typeof currentWorkspace,
    WorkspaceUser[]
    // Derived stores are initialized with undefined
>(
    currentWorkspace,
    ($currentWorkspace: Workspace | undefined, set) => {
        if (!$currentWorkspace) {
            return;
        }
        if (!$currentWorkspace.workspace_users) {
            throw new Error("Expected $currentWorkspace.workspace_users");
        }
        set($currentWorkspace.workspace_users);
    },
    [],
);

type CurrentWorkspaceUser = Readable<WorkspaceUser | undefined>;

/**
 * Find current workspace user belonging to logged in user
 */
export const currentWorkspaceUser: CurrentWorkspaceUser = derived<
    [typeof currentUser, typeof currentWorkspace],
    WorkspaceUser | undefined
>(
    [currentUser, currentWorkspace],
    ([$user, $currentWorkspace], set) => {
        if ($user === undefined || $currentWorkspace === undefined) {
            set(undefined);
            return;
        }
        const wsUser = $currentWorkspace.workspace_users.find(
            (wsUser) => wsUser.user.email === $user.email,
        );
        if (wsUser === undefined) {
            throw new Error("Couldn't find currentWorkspaceUser");
        }
        set(wsUser);
    },
    undefined,
);

type CurrentWorkspaceUserCan = Readable<
    (verb: Verb, resource: Resource) => boolean
>;

/**
 * A store that returns a function that allows permission checking for the
 * currently active, logged in user's workspace user.
 */
export const currentWorkspaceUserCan: CurrentWorkspaceUserCan = derived<
    [CurrentWorkspaceUser, typeof currentWorkspace],
    (verb: Verb, resource: Resource) => boolean
>(
    [currentWorkspaceUser, currentWorkspace],
    ([$currentWorkspaceUser, $currentWorkspace], set) => {
        if ($currentWorkspaceUser === undefined) {
            console.warn("workspaceUser was undefined");
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
                $currentWorkspaceUser,
                $currentWorkspace.quota,
            );
        set(fn);
    },
    () => false,
);
