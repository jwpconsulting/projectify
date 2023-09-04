import type { PageLoadEvent } from "./$types";

import { currentWorkspace } from "$lib/stores/dashboard";
import type { Workspace } from "$lib/types/workspace";

interface Data {
    workspace: Workspace;
}

export async function load({
    params: { workspaceUuid },
}: PageLoadEvent): Promise<Data> {
    const workspace = await currentWorkspace.loadUuid(workspaceUuid);
    return { workspace };
}
