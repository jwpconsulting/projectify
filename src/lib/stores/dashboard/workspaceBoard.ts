import { writable } from "svelte/store";

import { getWorkspaceBoard } from "$lib/repository/workspace";
import { createWsStore } from "$lib/stores/util";
import type { WorkspaceBoard } from "$lib/types/workspace";

const currentWorkspaceBoardUuid = writable<string | null>(null);

export const currentWorkspaceBoard = createWsStore<WorkspaceBoard>(
    "workspace-board",
    currentWorkspaceBoardUuid,
    getWorkspaceBoard
);
