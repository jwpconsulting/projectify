import { derived } from "svelte/store";

import { getArchivedWorkspaceBoards } from "$lib/repository/workspace";
import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import type { WorkspaceBoard } from "$lib/types/workspace";

export const currentArchivedWorkspaceBoards = derived<
    typeof currentWorkspace,
    WorkspaceBoard[]
>(currentWorkspace, ($currentWorkspace, set) => {
    const uuid = $currentWorkspace?.uuid;
    if (!uuid) {
        return;
    }
    getArchivedWorkspaceBoards(uuid, { fetch })
        .then(set)
        .catch((error: Error) => {
            console.error(
                "An error happened when retrieving currentArchivedWorkspaceBoards",
                { error }
            );
        });
});
