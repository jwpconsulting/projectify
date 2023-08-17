import { writable } from "svelte/store";

import { getWorkspace, getWorkspaces } from "$lib/repository/workspace";
import { currentWorkspaceBoard } from "$lib/stores/dashboard/workspaceBoard";
import { createWsStore } from "$lib/stores/util";
import type { Workspace, WorkspaceBoard } from "$lib/types/workspace";

export const workspaces = writable<Workspace[] | null>(null);

export const currentWorkspaceUuid = writable<string | null>(null);

export const currentWorkspace = createWsStore<Workspace>(
    "workspace",
    currentWorkspaceUuid,
    getWorkspace
);

currentWorkspaceBoard.subscribe(
    ($currentWorkspaceBoard: WorkspaceBoard | null) => {
        if (!$currentWorkspaceBoard) {
            return;
        }
        const { workspace } = $currentWorkspaceBoard;
        if (!workspace) {
            throw new Error("Expected $currentWorkspaceBoard.workspace");
        }
        const { uuid: workspaceUuid } = workspace;
        currentWorkspaceUuid.update(
            ($currentWorkspaceUuid: string | null): string | null => {
                // Is our current workspace uuid already set?
                // Is it equal to the current ws board's id?
                // Apparently, returning the same primitive value in a svelte
                // writable update will suppress subscriber callbacks
                // https://stackoverflow.com/questions/75525283/how-to-cancel-an-update-in-a-svelte-store
                if ($currentWorkspaceUuid == workspaceUuid) {
                    return $currentWorkspaceUuid;
                }
                console.log("Setting workspace UUID to", workspaceUuid);
                return workspaceUuid;
            }
        );
    }
);

export async function setWorkspaces() {
    workspaces.set(await getWorkspaces());
}

workspaces.subscribe(($workspaces: Workspace[] | null) => {
    if ($workspaces === null) {
        return;
    }
    let workspaceUuid;
    if ($workspaces.length) {
        workspaceUuid = $workspaces[0].uuid;
        currentWorkspaceUuid.set(workspaceUuid);
    } else {
        throw new Error("No workspaces");
    }
});

export async function setFirstWorkspace() {
    await setWorkspaces();
}
