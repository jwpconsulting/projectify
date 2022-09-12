export function getDashboardWorkspaceUrl(workspaceUuid: string) {
    return `/dashboard/workspace/${workspaceUuid}`;
}

export function getDashboardWorkspaceBoardUrl(workspaceBoardUuid: string) {
    return `/dashboard/workspace-board/${workspaceBoardUuid}`;
}

export function getDashboardTaskUrl(
    workspaceBoardUuid: string,
    taskUuid: string,
    view: string
) {
    return `/dashboard/workspace-board/${workspaceBoardUuid}?task=${taskUuid}&view=${view}`;
}

export function getSettingsUrl(
    workspaceUuid: string,
    kind: "index" | "labels" | "team-members"
) {
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
