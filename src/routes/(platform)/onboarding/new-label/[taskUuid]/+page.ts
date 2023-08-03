import type { PageLoadEvent } from "./$types";
import { getTask } from "$lib/repository/workspace";
import type {
    Task,
    Workspace,
    WorkspaceBoard,
    WorkspaceBoardSection,
} from "$lib/types/workspace";

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
    const { workspace_board_section: workspaceBoardSection } = task;
    if (!workspaceBoardSection) {
        throw new Error("Expected workspaceBoardSection");
    }
    const { workspace_board: workspaceBoard } = workspaceBoardSection;
    if (!workspaceBoard) {
        throw new Error("Expected workspaceBoard");
    }
    const { workspace } = workspaceBoard;
    if (!workspace) {
        throw new Error("Expected workspace");
    }
    return { task, workspaceBoardSection, workspaceBoard, workspace };
}
