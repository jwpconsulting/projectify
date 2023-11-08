import { error } from "@sveltejs/kit";

import {
    currentWorkspace,
    currentWorkspaceBoard,
    currentWorkspaces,
} from "$lib/stores/dashboard";
import type { Workspace, WorkspaceBoard } from "$lib/types/workspace";

import type { PageLoadEvent } from "./$types";

interface Data {
    workspaceBoard: WorkspaceBoard;
    workspace: Workspace;
    workspaces: Workspace[];
}

export async function load({
    params: { workspaceBoardUuid }, // TODO add fetch back and use in subscription somehow
    fetch,
}: PageLoadEvent): Promise<Data> {
    const workspaceBoard = await currentWorkspaceBoard.loadUuid(
        workspaceBoardUuid,
        { fetch }
    );
    if (!workspaceBoard) {
        throw error(404);
    }
    const workspaceUuid = workspaceBoard.workspace.uuid;
    if (!workspaceUuid) {
        throw new Error("Expected workspace");
    }
    const workspace = await currentWorkspace.loadUuid(workspaceUuid, {
        fetch,
    });
    if (!workspace) {
        throw error(404);
    }
    // XXX Might be able to do this asynchronously, meaning we don't need to wait
    // for it to finish here?
    const workspaces = await currentWorkspaces.load({ fetch });
    if (!workspaces) {
        throw error(404);
    }
    return { workspace, workspaceBoard, workspaces };
}
