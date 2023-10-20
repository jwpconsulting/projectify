import { error } from "@sveltejs/kit";

import { currentWorkspace } from "$lib/stores/dashboard";
import type { Workspace } from "$lib/types/workspace";

import type { LayoutLoadEvent } from "./$types";

interface Data {
    workspace: Workspace;
}

export async function load({
    params: { workspaceUuid },
    fetch,
}: LayoutLoadEvent): Promise<Data> {
    const workspace = await currentWorkspace.loadUuid(workspaceUuid, {
        fetch,
    });
    if (!workspace) {
        throw error(404);
    }
    return { workspace };
}
