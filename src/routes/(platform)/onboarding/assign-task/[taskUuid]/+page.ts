import { error } from "@sveltejs/kit";

import { currentTask } from "$lib/stores/dashboard";
import type {
    Label,
    Task,
    Workspace,
    WorkspaceBoard,
} from "$lib/types/workspace";
import { unwrap } from "$lib/utils/type";

import type { PageLoadEvent } from "./$types";

interface returnType {
    task: Task;
    workspaceBoard: WorkspaceBoard;
    workspace: Workspace;
    label: Label;
}
export async function load({
    fetch,
    params: { taskUuid },
}: PageLoadEvent): Promise<returnType> {
    const task = await currentTask.loadUuid(taskUuid, { fetch });
    if (!task) {
        throw error(404);
    }
    const workspaceBoard = task.workspace_board_section.workspace_board;
    const { workspace } = workspaceBoard;
    const label = unwrap(task.labels.at(0), "Expected label");
    return { task, workspaceBoard, workspace, label };
}
