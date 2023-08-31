import { getWorkspace } from "$lib/repository/workspace";
import { createWsStore } from "$lib/stores/util";
import type { Workspace } from "$lib/types/workspace";

export const currentWorkspace = createWsStore<Workspace>(
    "workspace",
    getWorkspace
);
