// TODO it seems like we could bundle all these [taskUuid] dependent onboarding
// pages like so:
// onboarding/task/[taskUuid]/new-label/
import { error } from "@sveltejs/kit";

import { getTask } from "$lib/repository/workspace";
import { getWorkspaceBoard } from "$lib/repository/workspace/workspaceBoard";
import type {
    TaskWithWorkspaceBoardSection,
    Workspace,
    WorkspaceBoardDetail,
    WorkspaceBoardSection,
} from "$lib/types/workspace";

import type { PageLoadEvent } from "./$types";

interface returnType {
    task: TaskWithWorkspaceBoardSection;
    workspaceBoardSection: WorkspaceBoardSection;
    workspaceBoard: WorkspaceBoardDetail;
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
    const { workspace_board_section: workspaceBoardSection } = task;
    const workspaceBoardUuid =
        task.workspace_board_section.workspace_board.uuid;
    const workspaceBoard = await getWorkspaceBoard(workspaceBoardUuid, {
        fetch,
    });
    if (!workspaceBoard) {
        throw new Error("Expected workspaceBoard");
    }
    const { workspace } = workspaceBoard;
    return { task, workspaceBoardSection, workspaceBoard, workspace };
}
