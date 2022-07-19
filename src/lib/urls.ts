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
