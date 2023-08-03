import type { PageLoadEvent } from "./$types";
import { getWorkspaceBoard } from "$lib/repository/workspace";
import type { Workspace, WorkspaceBoard } from "$lib/types/workspace";

export async function load({
    params: { workspaceBoardUuid },
    fetch,
}: PageLoadEvent): Promise<{
    workspaceBoard: WorkspaceBoard;
    workspace: Workspace;
}> {
    const workspaceBoard = await getWorkspaceBoard(workspaceBoardUuid, {
        fetch,
    });
    const { workspace } = workspaceBoard;
    if (!workspace) {
        throw new Error("Expected workspaceBoard");
    }
    return { workspaceBoard, workspace };
}
