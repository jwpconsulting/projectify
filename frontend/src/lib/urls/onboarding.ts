// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
export const startUrl = "/onboarding/welcome";

export const aboutYouUrl = "/onboarding/about-you";

export const newWorkspaceUrl = "/onboarding/new-workspace";
// TODO type these with workspace / section etc. instances
export function getNewProjectUrl(workspaceUuid: string): string {
    return `/onboarding/new-project/${workspaceUuid}`;
}

export function getNewTaskUrl(projectUuid: string): string {
    return `/onboarding/new-task/${projectUuid}`;
}

export function getNewLabelUrl(taskUuid: string): string {
    return `/onboarding/new-label/${taskUuid}`;
}

export function getAssignTaskUrl(taskUuid: string): string {
    return `/onboarding/assign-task/${taskUuid}`;
}
