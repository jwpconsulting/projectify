import type { PageLoadEvent } from "./$types";
import { currentWorkspaceBoardUuid } from "$lib/stores/dashboard";
import type { Workspace, WorkspaceBoard } from "$lib/types/workspace";
import { getWorkspaceBoard } from "$lib/repository/workspace";

interface Data {
    workspaceBoard: WorkspaceBoard;
    workspace: Workspace;
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
    return { workspace, workspaceBoard };
}
