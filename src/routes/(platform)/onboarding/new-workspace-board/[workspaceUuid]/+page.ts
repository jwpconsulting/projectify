import { error } from "@sveltejs/kit";

import { getWorkspace } from "$lib/repository/workspace";
import type { Workspace, WorkspaceBoard } from "$lib/types/workspace";

import type { PageLoadEvent } from "./$types";

export async function load({
    params: { workspaceUuid },
    fetch,
}: PageLoadEvent): Promise<{
    workspace: Workspace;
    workspaceBoard?: WorkspaceBoard;
}> {
    const workspace = await getWorkspace(workspaceUuid, { fetch });
    if (!workspace) {
        throw error(404);
    }
    const workspaceBoard = workspace.workspace_boards?.at(0);
    return { workspace, workspaceBoard };
}
