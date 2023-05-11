import { derived, writable } from "svelte/store";
import type { WSSubscriptionStore } from "$lib/stores/wsSubscription";
import type { Workspace } from "$lib/types/workspace";
import { browser } from "$app/environment";
import { getWorkspace, getWorkspaces } from "$lib/repository/workspace";
import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";

import { currentWorkspaceBoard } from "$lib/stores/dashboard/workspaceBoard";

export const workspaces = writable<Workspace[] | null>(null);

export const currentWorkspaceUuid = writable<string | null>(null);

let currentWorkspaceSubscription: WSSubscriptionStore | null = null;
let currentWorkspaceSubscriptionUnsubscribe: (() => void) | null = null;

export const currentWorkspace = derived<
    [typeof currentWorkspaceUuid],
    Workspace | null
>(
    [currentWorkspaceUuid],
    ([$currentWorkspaceUuid], set) => {
        if (!browser) {
            set(null);
            return;
        }
        if (!$currentWorkspaceUuid) {
            set(null);
            return;
        }
        set(null);
        getWorkspace($currentWorkspaceUuid)
            .then((workspace) => set(workspace))
            .catch((error: Error) => {
                console.error(
                    "An error happened when fetching $currentWorkspace",
                    { error }
                );
            });
        if (currentWorkspaceSubscriptionUnsubscribe) {
            currentWorkspaceSubscriptionUnsubscribe();
        }
        currentWorkspaceSubscription = getSubscriptionForCollection(
            "workspace",
            $currentWorkspaceUuid
        );
        if (!currentWorkspaceSubscription) {
            throw new Error("Expected currentWorkspaceSubscription");
        }
        currentWorkspaceSubscriptionUnsubscribe =
            currentWorkspaceSubscription.subscribe(async (_value) => {
                console.log("Refetching workspace", $currentWorkspaceUuid);
                set(await getWorkspace($currentWorkspaceUuid));
            });
    },
    null
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
