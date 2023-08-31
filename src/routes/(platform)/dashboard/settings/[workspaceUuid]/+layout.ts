import type { LayoutLoadEvent } from "./$types";

import { currentWorkspace } from "$lib/stores/dashboard";
import type { Workspace } from "$lib/types/workspace";

export const ssr = false;
export const prerender = false;

interface Data {
    workspace: Workspace;
}

export async function load({
    params: { workspaceUuid },
}: LayoutLoadEvent): Promise<Data> {
    const workspace = await currentWorkspace.loadUuid(workspaceUuid);
    return { workspace };
}
