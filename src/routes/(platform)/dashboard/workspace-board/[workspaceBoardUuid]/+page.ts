import type { PageLoadEvent } from "./$types";

import { getWorkspaceBoard, getWorkspaces } from "$lib/repository/workspace";
import { currentWorkspaceBoardUuid } from "$lib/stores/dashboard";
import type { Workspace, WorkspaceBoard } from "$lib/types/workspace";

interface Data {
    workspaceBoard: WorkspaceBoard;
    workspace: Workspace;
    workspaces: Workspace[];
}
export const prerender = false;
export const ssr = false;

export async function load({
    params: { workspaceBoardUuid },
    fetch,
}: PageLoadEvent): Promise<Data> {
    const workspaceBoard = await getWorkspaceBoard(workspaceBoardUuid, {
        fetch,
    });
    const { workspace } = workspaceBoard;
    if (!workspace) {
        throw new Error("Expected workspace");
    }
    currentWorkspaceBoardUuid.set(workspaceBoardUuid);
    // Might be able to do this asynchronously, meaning we don't need to wait
    // for it to finish here?
    const workspaces = await getWorkspaces();
    return { workspace, workspaceBoard, workspaces };
}
