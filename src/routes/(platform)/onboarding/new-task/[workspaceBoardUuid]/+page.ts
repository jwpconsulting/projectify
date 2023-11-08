import { error } from "@sveltejs/kit";

import { getWorkspace } from "$lib/repository/workspace";
import { getWorkspaceBoard } from "$lib/repository/workspace/workspaceBoard";
import type {
    WorkspaceBoard,
    WorkspaceBoardSection,
    WorkspaceDetail,
} from "$lib/types/workspace";

import type { PageLoadEvent } from "./$types";

export async function load({
    params: { workspaceBoardUuid },
    fetch,
}: PageLoadEvent): Promise<{
    workspaceBoard: WorkspaceBoard;
    workspace: WorkspaceDetail;
    workspaceBoardSection?: WorkspaceBoardSection;
}> {
    const workspaceBoard = await getWorkspaceBoard(workspaceBoardUuid, {
        fetch,
    });
    if (!workspaceBoard) {
        throw error(404);
    }
    const { uuid: workspaceUuid } = workspaceBoard.workspace;
    const workspace = await getWorkspace(workspaceUuid, {
        fetch,
    });
    if (!workspace) {
        throw error(404);
    }
    const workspaceBoardSection =
        workspaceBoard.workspace_board_sections.at(0);
    return { workspaceBoard, workspace, workspaceBoardSection };
}
