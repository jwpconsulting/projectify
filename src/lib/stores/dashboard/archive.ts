import { derived } from "svelte/store";

import { getArchivedWorkspaceBoards } from "$lib/repository/workspace";
import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import type { WorkspaceBoard } from "$lib/types/workspace";

export const currentArchivedWorkspaceBoards = derived<
    [typeof currentWorkspace],
    WorkspaceBoard[]
>(
    [currentWorkspace],
    ([$currentWorkspace], set) => {
        set([]);
        if (!$currentWorkspace) {
            return;
        }
        getArchivedWorkspaceBoards($currentWorkspace.uuid)
            .then((archivedWorkspaceBoards) => set(archivedWorkspaceBoards))
            .catch((error: Error) => {
                console.error(
                    "An error happened when retrieving currentArchivedWorkspaceBoards",
                    { error }
                );
            });
    },
    []
);
