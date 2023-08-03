// TODO type these with workspace / workspace board section etc. instances
export function getNewWorkspaceBoardUrl(workspaceUuid: string): string {
    return `/user/onboarding/new-workspace-board/${workspaceUuid}`;
}

export function getNewTaskUrl(workspaceBoardSectionUuid: string): string {
    return `/user/onboarding/new-task/${workspaceBoardSectionUuid}`;
}

export function getNewLabelUrl(taskUuid: string): string {
    return `/user/onboarding/new-label/${taskUuid}`;
}

export function getAssignTaskUrl(taskUuid: string): string {
    return `/user/onboarding/assign-task/${taskUuid}`;
}
