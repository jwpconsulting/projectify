import { writable } from "svelte/store";
import type { WorkspaceBoard } from "$lib/types/workspace";
import { getWorkspaceBoard } from "$lib/repository/workspace";
import { createWsStore } from "$lib/stores/util";

export const currentWorkspaceBoardUuid = writable<string | null>(null);

export const currentWorkspaceBoard = createWsStore<WorkspaceBoard>(
    "workspace-board",
    currentWorkspaceBoardUuid,
    getWorkspaceBoard
);
