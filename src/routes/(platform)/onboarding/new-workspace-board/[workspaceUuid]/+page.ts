import type { PageLoadEvent } from "./$types";

import { getWorkspace } from "$lib/repository/workspace";
import type { Workspace, WorkspaceBoard } from "$lib/types/workspace";

export async function load({
    params: { workspaceUuid },
    fetch,
}: PageLoadEvent): Promise<{
    workspace: Workspace;
    workspaceBoard?: WorkspaceBoard;
}> {
    const workspace = await getWorkspace(workspaceUuid, { fetch });
    const workspaceBoard = workspace.workspace_boards?.at(0);
    return { workspace, workspaceBoard };
}
