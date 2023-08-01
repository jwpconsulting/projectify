import type { PageLoadEvent } from "./$types";
import { getWorkspaces } from "$lib/repository/workspace";
import type { Workspace } from "$lib/types/workspace";

export async function load({
    fetch,
}: PageLoadEvent): Promise<{ workspace?: Workspace }> {
    const workspaces = await getWorkspaces({ fetch });
    const workspace = workspaces.length > 0 ? workspaces[0] : undefined;
    return { workspace };
}
