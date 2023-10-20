// TODO it seems like we could bundle all these [taskUuid] dependent onboarding
// pages like so:
// onboarding/task/[taskUuid]/new-label/
import { error } from "@sveltejs/kit";

import { getTask } from "$lib/repository/workspace";
import type {
    Task,
    Workspace,
    WorkspaceBoard,
    WorkspaceBoardSection,
} from "$lib/types/workspace";

import type { PageLoadEvent } from "./$types";

interface returnType {
    task: Task;
    workspaceBoardSection: WorkspaceBoardSection;
    workspaceBoard: WorkspaceBoard;
    workspace: Workspace;
}

export async function load({
    fetch,
    params: { taskUuid },
}: PageLoadEvent): Promise<returnType> {
    const task = await getTask(taskUuid, { fetch });
    if (!task) {
        throw error(404);
    }
    return {
        task,
        workspaceBoardSection: task.workspace_board_section,
        workspaceBoard: task.workspace_board_section.workspace_board,
        workspace: task.workspace_board_section.workspace_board.workspace,
    };
}
