// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2024 JWP Consulting GK
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

import type { WorkspaceUser, WorkspaceUserRole } from "$lib/types/workspace";

/**
 * Functions for permission checking, see rules in Django backend
 *
 * The permission checking is not security relevant and only serves cosmetic
 * purposes. We check for the actual permissions in the backend, but would not
 * like to offer the user to perform actions that will then just fail in the
 * backend when making an API request.
 */
export type Verb = "create" | "read" | "update" | "delete";
export type Resource =
    | "workspace"
    | "workspaceUserInvite"
    | "workspaceUser"
    | "workspaceBoard"
    | "workspaceBoardSection"
    | "task"
    | "label"
    | "taskLabel"
    | "subTask"
    | "chatMessage"
    | "customer";

type CrudMinimumRole = {
    [K in Verb]: WorkspaceUserRole;
};

type Rules = {
    [K in Resource]: CrudMinimumRole;
};

/**
 * Referencing docs/rules.md
| Resource                | Create     | Read       | Update     | Delete     |
|-------------------------|------------|------------|------------|------------|
| Workspace               | Owner      | Observer   | Owner      | Owner      |
| Workspace user invite   | Owner      | Owner      | Owner      | Owner      |
| Workspace user          | Owner      | Observer   | Owner      | Owner      |
| Workspace board         | Maintainer | Observer   | Maintainer | Maintainer |
| Workspace board section | Maintainer | Observer   | Maintainer | Maintainer |
| Task                    | Member     | Observer   | Member     | Maintainer |
| Label                   | Maintainer | Observer   | Maintainer | Maintainer |
| Task label              | Member     | Observer   | Member     | Member     |
| Sub task                | Member     | Observer   | Member     | Member     |
| Chat message            | Member     | Observer   | Member     | Maintainer |
| Customer                | Owner      | Owner      | Owner      | Owner      |
 */

const rules: Rules = {
    workspace: {
        create: "OWNER",
        read: "OBSERVER",
        update: "OWNER",
        delete: "OWNER",
    },
    workspaceUserInvite: {
        create: "OWNER",
        read: "OWNER",
        update: "OWNER",
        delete: "OWNER",
    },
    workspaceUser: {
        create: "OWNER",
        read: "OBSERVER",
        update: "OWNER",
        delete: "OWNER",
    },
    workspaceBoard: {
        create: "MAINTAINER",
        read: "OBSERVER",
        update: "MAINTAINER",
        delete: "MAINTAINER",
    },
    workspaceBoardSection: {
        create: "MAINTAINER",
        read: "OBSERVER",
        update: "MAINTAINER",
        delete: "MAINTAINER",
    },
    task: {
        create: "MEMBER",
        read: "OBSERVER",
        update: "MEMBER",
        delete: "MAINTAINER",
    },
    label: {
        create: "MAINTAINER",
        read: "OBSERVER",
        update: "MAINTAINER",
        delete: "MAINTAINER",
    },
    taskLabel: {
        create: "MEMBER",
        read: "OBSERVER",
        update: "MEMBER",
        delete: "MEMBER",
    },
    subTask: {
        create: "MEMBER",
        read: "OBSERVER",
        update: "MEMBER",
        delete: "MEMBER",
    },
    chatMessage: {
        create: "MEMBER",
        read: "OBSERVER",
        update: "MEMBER",
        delete: "MAINTAINER",
    },
    customer: {
        create: "OWNER",
        read: "OWNER",
        update: "OWNER",
        delete: "OWNER",
    },
};

/**
 * Total ordering for roles. For a given role, is this role at least $ROLE?
 */
const isAtLeast: {
    [K in WorkspaceUserRole]: { [K in WorkspaceUserRole]: boolean };
} = {
    OBSERVER: {
        OBSERVER: true,
        MEMBER: false,
        MAINTAINER: false,
        OWNER: false,
    },
    MEMBER: {
        OBSERVER: true,
        MEMBER: true,
        MAINTAINER: false,
        OWNER: false,
    },
    MAINTAINER: {
        OBSERVER: true,
        MEMBER: true,
        MAINTAINER: true,
        OWNER: false,
    },
    OWNER: {
        OBSERVER: true,
        MEMBER: true,
        MAINTAINER: true,
        OWNER: true,
    },
};

// TODO check trial limits as well for create actions
export function can(
    verb: Verb,
    resource: Resource,
    { role }: Pick<WorkspaceUser, "role">,
): boolean {
    const minimum = rules[resource][verb];
    return isAtLeast[role][minimum];
}
