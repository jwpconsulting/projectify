import type { LayoutLoadEvent } from "./$types";

import {
    currentTask,
    currentWorkspaceUuid,
    currentTaskUuid,
} from "$lib/stores/dashboard";
import type {
    Task,
    Workspace,
    WorkspaceBoard,
    WorkspaceBoardSection,
} from "$lib/types/workspace";

export const prerender = false;
export const ssr = false;

interface Data {
    task: Task;
    workspaceBoardSection: WorkspaceBoardSection;
    workspaceBoard: WorkspaceBoard;
    workspace: Workspace;
}

export async function load({
    params: { taskUuid },
}: LayoutLoadEvent): Promise<Data> {
    currentTaskUuid.set(taskUuid);
    return new Promise<Data>((resolve) => {
        currentTask.subscribe(($currentTask) => {
            if (!$currentTask) {
                return;
            }
            const { workspace_board_section: workspaceBoardSection } =
                $currentTask;
            if (!workspaceBoardSection) {
                throw new Error("Expected workspace_board_section");
            }
            const { workspace_board: workspaceBoard } = workspaceBoardSection;
            if (!workspaceBoard) {
                throw new Error("Expected workspace_board");
            }
            const { workspace } = workspaceBoard;
            if (!workspace) {
                throw new Error("Expected workspace");
            }
            currentWorkspaceUuid.set(workspace.uuid);
            resolve({
                task: $currentTask,
                workspaceBoardSection,
                workspaceBoard,
                workspace,
            });
        });
    });
}
