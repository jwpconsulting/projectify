// TODO type these with workspace / workspace board section etc. instances
export function getNewWorkspaceBoardUrl(workspaceUuid: string): string {
    return `/onboarding/new-workspace-board/${workspaceUuid}`;
}

export function getNewTaskUrl(workspaceBoardSectionUuid: string): string {
    return `/onboarding/new-task/${workspaceBoardSectionUuid}`;
}

export function getNewLabelUrl(taskUuid: string): string {
    return `/onboarding/new-label/${taskUuid}`;
}

export function getAssignTaskUrl(taskUuid: string): string {
    return `/onboarding/assign-task/${taskUuid}`;
}
