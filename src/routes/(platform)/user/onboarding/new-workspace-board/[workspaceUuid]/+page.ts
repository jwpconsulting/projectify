import type { PageLoadEvent } from "./$types";
import { getWorkspace, getWorkspaceBoard } from "$lib/repository/workspace";
import type {
    Workspace,
    WorkspaceBoard,
    WorkspaceBoardSection,
} from "$lib/types/workspace";

export async function load({
    params: { workspaceUuid },
    fetch,
}: PageLoadEvent): Promise<{
    workspace: Workspace;
    workspaceBoard?: WorkspaceBoard;
    workspaceBoardSection?: WorkspaceBoardSection;
}> {
    const workspace = await getWorkspace(workspaceUuid, { fetch });
    const workspaceBoard = workspace.workspace_boards?.at(0);
    const workspaceBoardSection =
        workspaceBoard &&
        (
            await getWorkspaceBoard(workspaceBoard.uuid)
        ).workspace_board_sections?.at(0);
    return { workspace, workspaceBoard, workspaceBoardSection };
}
