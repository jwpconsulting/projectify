// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import type { SettingKind } from "$lib/types/dashboard";
import type {
    ProjectDetail,
    TaskDetailSection,
    Task,
    WorkspaceDetail,
} from "$lib/types/workspace";

// This will be shown every time we suggest the user to go "back to home"
// or similar
export const backToHomeUrl = "/";

// TODO put me into dashboard urls
export function getDashboardWorkspaceUrl({
    uuid,
}: Pick<WorkspaceDetail, "uuid">) {
    return `/dashboard/workspace/${uuid}`;
}

// TODO put me into dashboard urls
export function getDashboardProjectUrl({ uuid }: Pick<ProjectDetail, "uuid">) {
    return `/dashboard/project/${uuid}`;
}

// TODO put me into dashboard urls
export function getDashboardSectionUrl({
    uuid,
}: Pick<TaskDetailSection, "uuid">) {
    return `/dashboard/section/${uuid}`;
}

// TODO put me into dashboard urls
export function getSettingsUrl(
    { uuid }: Pick<WorkspaceDetail, "uuid">,
    kind: SettingKind,
) {
    const suffix = {
        "index": "",
        "team-members": "/team-members",
        "billing": "/billing",
        "quota": "/quota",
    }[kind];
    return `/dashboard/workspace/${uuid}/settings${suffix}`;
}

// TODO put me into dashboard urls
export function getArchiveUrl({ uuid }: Pick<WorkspaceDetail, "uuid">) {
    return `/dashboard/workspace/${uuid}/archive`;
}

// TODO put me into auth routes
// Doesn't have to a function, can just be const string
export function getProfileUrl() {
    return "/user/profile";
}

// TODO put me into dashboard urls
export function getNewTaskUrl({ uuid }: Pick<TaskDetailSection, "uuid">) {
    return `/dashboard/section/${uuid}/create-task`;
}

// TODO put me into dashboard urls
export function getTaskUrl({ uuid }: Pick<Task, "uuid">) {
    return `/dashboard/task/${uuid}`;
}

// TODO put me into dashboard urls
export function getTaskEditUrl({ uuid }: Pick<Task, "uuid">) {
    return `/dashboard/task/${uuid}/update`;
}
