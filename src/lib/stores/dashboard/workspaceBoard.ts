import { derived, writable } from "svelte/store";
import type { WorkspaceBoard } from "$lib/types/workspace";
import { browser } from "$app/environment";
import type { WSSubscriptionStore } from "$lib/stores/wsSubscription";
import { getWorkspaceBoard } from "$lib/repository/workspace";
import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";

export const currentWorkspaceBoardUuid = writable<string | null>(null);
let currentWorkspaceBoardSubscription: WSSubscriptionStore | null = null;
let currentWorkspaceBoardSubscriptionUnsubscribe: (() => void) | null = null;

export const currentWorkspaceBoard = derived<
    [typeof currentWorkspaceBoardUuid],
    WorkspaceBoard | null
>([currentWorkspaceBoardUuid], ([$currentWorkspaceBoardUuid], set) => {
    if (!browser) {
        set(null);
        return;
    }
    if (!$currentWorkspaceBoardUuid) {
        set(null);
        return;
    }
    set(null);
    getWorkspaceBoard($currentWorkspaceBoardUuid)
        .then((workspaceBoard) => set(workspaceBoard))
        .catch((error: Error) => {
            console.error(
                "An error happened when fetching $currentWorkspaceBoard",
                { error }
            );
        });
    if (currentWorkspaceBoardSubscriptionUnsubscribe) {
        currentWorkspaceBoardSubscriptionUnsubscribe();
    }
    currentWorkspaceBoardSubscription = getSubscriptionForCollection(
        "workspace-board",
        $currentWorkspaceBoardUuid
    );
    if (!currentWorkspaceBoardSubscription) {
        throw new Error("Expected currentWorkspaceBoardSubscription");
    }
    currentWorkspaceBoardSubscriptionUnsubscribe =
        currentWorkspaceBoardSubscription.subscribe(async (_value) => {
            console.log(
                "Refetching workspaceBoard",
                $currentWorkspaceBoardUuid
            );
            set(await getWorkspaceBoard($currentWorkspaceBoardUuid));
        });
});
