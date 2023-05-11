import type { PageLoadEvent } from "./$types";
import { currentWorkspaceBoardUuid } from "$lib/stores/dashboard";
import type { WorkspaceBoard } from "$lib/types/workspace";
import { getWorkspaceBoard } from "$lib/repository/workspace";

type Data = {
    workspaceBoard: WorkspaceBoard;
};
export const prerender = false;
export const ssr = false;

export async function load({
    params: { workspaceBoardUuid },
    fetch,
}: PageLoadEvent): Promise<Data> {
    const workspaceBoard = await getWorkspaceBoard(workspaceBoardUuid, {
        fetch,
    });
    currentWorkspaceBoardUuid.set(workspaceBoardUuid);
    return { workspaceBoard };
}
