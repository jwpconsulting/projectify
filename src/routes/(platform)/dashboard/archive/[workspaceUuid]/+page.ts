import { currentWorkspace } from "$lib/stores/dashboard";
import type { Workspace } from "$lib/types/workspace";

import type { PageLoadEvent } from "./$types";

interface Data {
    workspace: Workspace;
}

export async function load({
    params: { workspaceUuid },
    fetch,
}: PageLoadEvent): Promise<Data> {
    const workspace = await currentWorkspace.loadUuid(workspaceUuid, {
        fetch,
    });
    return { workspace };
}
