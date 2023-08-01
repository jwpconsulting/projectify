export function getNewWorkspaceBoardUrl(workspaceUuid: string): string {
    return `/user/onboarding/new-workspace-board/${workspaceUuid}`;
}

export function getNewTaskUrl(workspaceBoardSectionUuid: string): string {
    return `/user/onboarding/new-task/${workspaceBoardSectionUuid}`;
}
