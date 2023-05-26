import { derived, writable } from "svelte/store";
import { createWsStore } from "$lib/stores/util";
import type { Workspace } from "$lib/types/workspace";
import { getWorkspace, getWorkspaces } from "$lib/repository/workspace";

import { currentWorkspaceBoard } from "$lib/stores/dashboard/workspaceBoard";

export const workspaces = writable<Workspace[] | null>(null);

export const currentWorkspaceUuid = writable<string | null>(null);

export const currentWorkspace = createWsStore<Workspace>(
    "workspace",
    currentWorkspaceUuid,
    getWorkspace
);

const ensureWorkspaceUuid = derived<
    [typeof currentWorkspaceUuid, typeof currentWorkspaceBoard],
    string | null
>(
    [currentWorkspaceUuid, currentWorkspaceBoard],
    ([$currentWorkspaceUuid, $currentWorkspaceBoard], set) => {
        // $currentWorkspaceUuid has already been set
        if ($currentWorkspaceUuid) {
            return;
        }
        if (!$currentWorkspaceBoard) {
            return;
        }
        if (!$currentWorkspaceBoard.workspace) {
            console.error("Expected $currentWorkspaceBoard.workspace");
            return;
        }
        const { uuid } = $currentWorkspaceBoard.workspace;
        console.log("Setting workspace UUID to", uuid);
        set(uuid);
    },
    null
);
ensureWorkspaceUuid.subscribe((workspaceUuid: string | null) => {
    if (!workspaceUuid) {
        return;
    }
    currentWorkspaceUuid.set(workspaceUuid);
});

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
