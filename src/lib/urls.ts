import type { SettingKind } from "$lib/types/dashboard";

export function getDashboardWorkspaceUrl(workspaceUuid: string) {
    return `/dashboard/workspace/${workspaceUuid}`;
}

export function getDashboardWorkspaceBoardUrl(workspaceBoardUuid: string) {
    return `/dashboard/workspace-board/${workspaceBoardUuid}`;
}

export function getDashboardWorkspaceBoardSectionUrl(
    workspaceBoardSectionUuid: string
) {
    return `/dashboard/workspace-board-section/${workspaceBoardSectionUuid}`;
}

export function getDashboardTaskUrl(
    workspaceBoardUuid: string,
    taskUuid: string,
    view: string
) {
    return `/dashboard/workspace-board/${workspaceBoardUuid}?task=${taskUuid}&view=${view}`;
}

export function getSettingsUrl(workspaceUuid: string, kind: SettingKind) {
    const root = `/dashboard/settings/${workspaceUuid}`;
    if (kind === "index") {
        return root;
    }
    return `${root}/${kind}`;
}

export function getArchiveUrl(workspaceUuid: string) {
    return `/dashboard/archive/${workspaceUuid}`;
}

export function getProfileUrl() {
    return "/user/profile";
}

export function getNewTaskUrl(workspaceBoardSectionUuid: string) {
    return `/dashboard/workspace-board-section/${workspaceBoardSectionUuid}/new-task`;
}
