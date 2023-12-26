import type { SettingKind } from "$lib/types/dashboard";

// This will be shown every time we suggest the user to go "back to home"
// or similar
export const backToHomeUrl = "/";

// TODO put me into dashboard urls
// TODO accept workspace directly
export function getDashboardWorkspaceUrl(workspaceUuid: string) {
    return `/dashboard/workspace/${workspaceUuid}`;
}

// TODO put me into dashboard urls
// TODO accept workspaceBoard directly
export function getDashboardWorkspaceBoardUrl(workspaceBoardUuid: string) {
    return `/dashboard/workspace-board/${workspaceBoardUuid}`;
}

// TODO put me into dashboard urls
export function getDashboardWorkspaceBoardSectionUrl(
    // TODO accept workspaceBoardSection directly
    workspaceBoardSectionUuid: string,
) {
    return `/dashboard/workspace-board-section/${workspaceBoardSectionUuid}`;
}

// TODO put me into dashboard urls
// TODO accept workspace directly
export function getSettingsUrl(workspaceUuid: string, kind: SettingKind) {
    const suffix = {
        "index": "",
        // TODO remove me
        "labels": "/labels",
        "workspace-users": "/workspace-users",
        "billing": "/billing",
    }[kind];
    return `/dashboard/workspace/${workspaceUuid}/settings${suffix}`;
}

// TODO put me into dashboard urls
// TODO accept workspace directly
export function getArchiveUrl(workspaceUuid: string) {
    return `/dashboard/workspace/${workspaceUuid}/archive`;
}

// TODO put me into auth routes
export function getProfileUrl() {
    return "/user/profile";
}

// TODO put me into dashboard urls
// TODO accept workspaceBoardSection directly
export function getNewTaskUrl(workspaceBoardSectionUuid: string) {
    return `/dashboard/workspace-board-section/${workspaceBoardSectionUuid}/create-task`;
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
