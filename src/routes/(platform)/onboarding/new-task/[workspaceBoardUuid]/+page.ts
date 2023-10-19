import {
    currentWorkspace,
    currentWorkspaceBoard,
} from "$lib/stores/dashboard";
import type {
    Workspace,
    WorkspaceBoard,
    WorkspaceBoardSection,
} from "$lib/types/workspace";
import { unwrap } from "$lib/utils/type";

import type { PageLoadEvent } from "./$types";

export async function load({
    params: { workspaceBoardUuid },
    fetch,
}: PageLoadEvent): Promise<{
    workspaceBoard: WorkspaceBoard;
    workspace: Workspace;
    workspaceBoardSection?: WorkspaceBoardSection;
}> {
    const workspaceBoard = await currentWorkspaceBoard.loadUuid(
        workspaceBoardUuid,
        {
            fetch,
        }
    );
    const { uuid: workspaceUuid } = unwrap(
        workspaceBoard.workspace,
        "Expected workspace"
    );
    const workspace = await currentWorkspace.loadUuid(workspaceUuid, {
        fetch,
    });
    const workspaceBoardSections =
        workspaceBoard.workspace_board_sections ?? [];
    const workspaceBoardSection = workspaceBoardSections.at(0);
    return { workspaceBoard, workspace, workspaceBoardSection };
}
