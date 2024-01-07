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
export const startUrl = "/onboarding/welcome";

export const aboutYouUrl = "/onboarding/about-you";

export const newWorkspaceUrl = "/onboarding/new-workspace";
// TODO type these with workspace / workspace board section etc. instances
export function getNewWorkspaceBoardUrl(workspaceUuid: string): string {
    return `/onboarding/new-workspace-board/${workspaceUuid}`;
}

export function getNewTaskUrl(workspaceBoardUuid: string): string {
    return `/onboarding/new-task/${workspaceBoardUuid}`;
}

export function getNewLabelUrl(taskUuid: string): string {
    return `/onboarding/new-label/${taskUuid}`;
}

export function getAssignTaskUrl(taskUuid: string): string {
    return `/onboarding/assign-task/${taskUuid}`;
}
