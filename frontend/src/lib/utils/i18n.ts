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
import type { WorkspaceUserRole } from "$lib/types/workspaceUserRole";
import { workspaceUserRoles } from "$lib/types/workspaceUserRole";

export function getMessageNameForRole(
    $_: (id: string) => string,
    role: string,
) {
    // This casting should be done further upstream
    // TODO Justus 2022-09-29
    if (!workspaceUserRoles.includes(role as WorkspaceUserRole)) {
        throw new Error(`Expected valid role, got ${role}`);
    }
    return {
        OBSERVER: $_("roles.observer"),
        MEMBER: $_("roles.member"),
        MAINTAINER: $_("roles.maintainer"),
        OWNER: $_("roles.owner"),
    }[role as WorkspaceUserRole];
}
