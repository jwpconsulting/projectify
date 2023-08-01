import type { PageLoadEvent } from "./$types";
import { getWorkspaces } from "$lib/repository/workspace";

export async function load({
    fetch,
}: PageLoadEvent): Promise<{ hasWorkspace: boolean }> {
    const workspaces = await getWorkspaces({ fetch });
    const hasWorkspace = workspaces.length > 0;
    return { hasWorkspace };
}
