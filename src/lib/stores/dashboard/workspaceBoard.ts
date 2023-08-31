import { getWorkspaceBoard } from "$lib/repository/workspace";
import { createWsStore } from "$lib/stores/wsSubscription";
import type { WorkspaceBoard } from "$lib/types/workspace";

export const currentWorkspaceBoard = createWsStore<WorkspaceBoard>(
    "workspace-board",
    getWorkspaceBoard
);
