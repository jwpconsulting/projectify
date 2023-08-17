import type { PageLoadEvent } from "./$types";

import { getTask } from "$lib/repository/workspace";
import type {
    Label,
    Task,
    Workspace,
    WorkspaceBoard,
} from "$lib/types/workspace";
import { unwrap } from "$lib/utils/type";

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
    const task = await getTask(taskUuid, { fetch });
    const workspaceBoard = unwrap(
        task.workspace_board_section?.workspace_board,
        "Expected workspaceBoard"
    );
    const workspace = unwrap(workspaceBoard.workspace, "Expected workspace");
    const label = unwrap(task.labels.at(0), "Expected label");
    return { task, workspaceBoard, workspace, label };
}
