import { writable } from "svelte/store";

import { getWorkspace } from "$lib/repository/workspace";
import { createWsStore } from "$lib/stores/util";
import type { Workspace } from "$lib/types/workspace";

export const currentWorkspaceUuid = writable<string | null>(null);

export const currentWorkspace = createWsStore<Workspace>(
    "workspace",
    currentWorkspaceUuid,
    getWorkspace
);
