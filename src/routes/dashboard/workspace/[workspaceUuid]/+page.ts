import { redirect } from "@sveltejs/kit";
import type { PageLoadEvent } from "./$types";
import type { Workspace } from "$lib/types/workspace";
import { getWorkspace } from "$lib/repository/workspace";
import { getDashboardWorkspaceBoardUrl } from "$lib/urls";

interface Data {
    workspace: Workspace;
}
export const prerender = false;
export const ssr = false;

export async function load({
    params: { workspaceUuid },
    fetch,
}: PageLoadEvent): Promise<Data> {
    const workspace = await getWorkspace(workspaceUuid, {
        fetch,
    });

    const { workspace_boards } = workspace;

    if (workspace_boards?.length) {
        const { uuid } = workspace_boards[0];
        // eslint-disable-next-line @typescript-eslint/no-throw-literal
        throw redirect(302, getDashboardWorkspaceBoardUrl(uuid));
    }
    // TODO
    console.error("TODO handle no workspace boards");
    return { workspace };
}
