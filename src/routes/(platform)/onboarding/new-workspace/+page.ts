import { error } from "@sveltejs/kit";

import { getWorkspaces } from "$lib/repository/workspace";
import type { Workspace } from "$lib/types/workspace";

import type { PageLoadEvent } from "./$types";

export async function load({
    fetch,
}: PageLoadEvent): Promise<{ workspace?: Workspace }> {
    const workspaces = await getWorkspaces({ fetch });
    if (!workspaces) {
        // Undefined workspaces is unrecoverable
        throw error(500);
    }
    const workspace = workspaces.length > 0 ? workspaces[0] : undefined;
    return { workspace };
}
