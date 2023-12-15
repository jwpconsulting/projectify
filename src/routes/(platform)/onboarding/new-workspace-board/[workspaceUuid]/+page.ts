import { error } from "@sveltejs/kit";

import { getWorkspace } from "$lib/repository/workspace";
import { getWorkspaceBoard } from "$lib/repository/workspace/workspaceBoard";
import type { Workspace, WorkspaceBoardDetail } from "$lib/types/workspace";

import type { PageLoadEvent } from "./$types";

export async function load({
    params: { workspaceUuid },
    fetch,
}: PageLoadEvent): Promise<{
    workspace: Workspace;
    workspaceBoard?: WorkspaceBoardDetail;
}> {
    const workspace = await getWorkspace(workspaceUuid, { fetch });
    if (!workspace) {
        throw error(404);
    }
    const workspaceBoardUuid = workspace.workspace_boards.at(0)?.uuid;
    const workspaceBoard = workspaceBoardUuid
        ? await getWorkspaceBoard(workspaceBoardUuid, { fetch })
        : undefined;
    return { workspace, workspaceBoard };
}
