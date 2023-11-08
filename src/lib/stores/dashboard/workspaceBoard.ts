import { getWorkspaceBoard } from "$lib/repository/workspace/workspaceBoard";
import { createWsStore } from "$lib/stores/wsSubscription";

export const currentWorkspaceBoard = createWsStore(
    "workspace-board",
    getWorkspaceBoard
);
