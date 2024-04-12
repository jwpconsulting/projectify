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
import type { SettingKind } from "$lib/types/dashboard";
import type { Project, Section } from "$lib/types/workspace";

// This will be shown every time we suggest the user to go "back to home"
// or similar
export const backToHomeUrl = "/";

// TODO put me into dashboard urls
// TODO accept workspace directly
export function getDashboardWorkspaceUrl(workspaceUuid: string) {
    return `/dashboard/workspace/${workspaceUuid}`;
}

// TODO put me into dashboard urls
export function getDashboardProjectUrl({ uuid }: Pick<Project, "uuid">) {
    return `/dashboard/project/${uuid}`;
}

// TODO put me into dashboard urls
export function getDashboardSectionUrl({ uuid }: Pick<Section, "uuid">) {
    return `/dashboard/section/${uuid}`;
}

// TODO put me into dashboard urls
// TODO accept workspace directly
export function getSettingsUrl(workspaceUuid: string, kind: SettingKind) {
    const suffix = {
        "index": "",
        "team-members": "/team-members",
        "billing": "/billing",
        "quota": "/quota",
    }[kind];
    return `/dashboard/workspace/${workspaceUuid}/settings${suffix}`;
}

// TODO put me into dashboard urls
// TODO accept workspace directly
export function getArchiveUrl(workspaceUuid: string) {
    return `/dashboard/workspace/${workspaceUuid}/archive`;
}

// TODO put me into auth routes
// Doesn't have to a function, can just be const string
export function getProfileUrl() {
    return "/user/profile";
}

// TODO put me into dashboard urls
// TODO accept section directly
export function getNewTaskUrl(sectionUuid: string) {
    return `/dashboard/section/${sectionUuid}/create-task`;
}

// TODO put me into dashboard urls
// TODO accept task directly
export function getTaskUrl(taskUuid: string) {
    return `/dashboard/task/${taskUuid}`;
}

// TODO put me into dashboard urls
// TODO accept task directly
export function getTaskEditUrl(taskUuid: string) {
    return `/dashboard/task/${taskUuid}/update`;
}
