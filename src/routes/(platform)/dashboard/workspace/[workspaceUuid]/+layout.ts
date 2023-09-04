import type { LayoutLoadEvent } from "./$types";

import { currentWorkspace } from "$lib/stores/dashboard";
import type { Workspace } from "$lib/types/workspace";

export const prerender = false;
export const ssr = false;

interface Data {
    workspace: Workspace;
}

export async function load({
    params: { workspaceUuid },
}: LayoutLoadEvent): Promise<Data> {
    const workspace = await currentWorkspace.loadUuid(workspaceUuid);
    return { workspace };
}
