import type { LayoutLoadEvent } from "./$types";

import { currentTask, currentWorkspace } from "$lib/stores/dashboard";
import type {
    Task,
    Workspace,
    WorkspaceBoard,
    WorkspaceBoardSection,
} from "$lib/types/workspace";
import { unwrap } from "$lib/utils/type";

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
    const task = await currentTask.loadUuid(taskUuid);
    const workspaceBoardSection = unwrap(
        task.workspace_board_section,
        "Expected workspace_board_section"
    );
    const workspaceBoard = unwrap(
        workspaceBoardSection.workspace_board,
        "Expected workspace_board"
    );

    const workspaceUuid = unwrap(
        workspaceBoard.workspace?.uuid,
        "Expected uuid"
    );
    const workspace = await currentWorkspace.loadUuid(workspaceUuid);
    return {
        task,
        workspaceBoardSection,
        workspaceBoard,
        workspace,
    };
}
