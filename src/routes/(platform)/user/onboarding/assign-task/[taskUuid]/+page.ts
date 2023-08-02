import type { PageLoadEvent } from "./$types";
import { getTask } from "$lib/repository/workspace";
import type {
    Label,
    Task,
    Workspace,
    WorkspaceBoard,
} from "$lib/types/workspace";

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
    const workspaceBoard = task.workspace_board_section?.workspace_board;
    if (!workspaceBoard) {
        throw new Error("Expected workspaceBoard");
    }
    const workspace = workspaceBoard.workspace;
    if (!workspace) {
        throw new Error("Expected workspace");
    }
    const label = task.labels.at(0);
    if (!label) {
        throw new Error("Expected label");
    }
    return { task, workspaceBoard, workspace, label };
}
