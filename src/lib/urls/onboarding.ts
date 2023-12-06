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
