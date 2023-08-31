import type { PageLoadEvent } from "./$types";

import { getWorkspaces } from "$lib/repository/workspace";
import {
    currentWorkspace,
    currentWorkspaceBoard,
} from "$lib/stores/dashboard";
import type { Workspace, WorkspaceBoard } from "$lib/types/workspace";

interface Data {
    workspaceBoard: WorkspaceBoard;
    workspace: Workspace;
    workspaces: Workspace[];
}
export const prerender = false;
export const ssr = false;

export async function load({
    params: { workspaceBoardUuid }, // TODO add fetch back and use in subscription somehow
}: PageLoadEvent): Promise<Data> {
    const workspaceBoard =
        await currentWorkspaceBoard.loadUuid(workspaceBoardUuid);
    const workspaceUuid = workspaceBoard.workspace?.uuid;
    if (!workspaceUuid) {
        throw new Error("Expected workspace");
    }
    const workspace = await currentWorkspace.loadUuid(workspaceUuid);
    // Might be able to do this asynchronously, meaning we don't need to wait
    // for it to finish here?
    const workspaces = await getWorkspaces();
    return { workspace, workspaceBoard, workspaces };
}
