import { error } from "@sveltejs/kit";

import {
    currentWorkspace,
    currentWorkspaceBoard,
} from "$lib/stores/dashboard";
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
    const workspaceBoard = await currentWorkspaceBoard.loadUuid(
        workspaceBoardUuid,
        {
            fetch,
        }
    );
    if (!workspaceBoard) {
        throw error(404);
    }
    const { uuid: workspaceUuid } = workspaceBoard.workspace;
    const workspace = await currentWorkspace.loadUuid(workspaceUuid, {
        fetch,
    });
    if (!workspace) {
        throw error(404);
    }
    const workspaceBoardSection =
        workspaceBoard.workspace_board_sections.at(0);
    return { workspaceBoard, workspace, workspaceBoardSection };
}
