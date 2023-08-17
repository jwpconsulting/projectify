import { redirect } from "@sveltejs/kit";

import { getDashboardWorkspaceBoardUrl } from "$lib/urls";

import { getWorkspaceBoardSection } from "$lib/repository/workspace";

export const prerender = false;
export const ssr = false;

export async function load({
    fetch,
    params,
}: {
    fetch: typeof window.fetch;
    params: { workspaceBoardSectionUuid: string };
}) {
    const workspaceBoardSection = await getWorkspaceBoardSection(
        params.workspaceBoardSectionUuid,
        { fetch }
    );
    const workspaceBoard = workspaceBoardSection.workspace_board;
    if (!workspaceBoard) {
        // Unlikely
        throw new Error("Expected workspaceBoard");
    }
    // eslint-disable-next-line @typescript-eslint/no-throw-literal
    throw redirect(302, getDashboardWorkspaceBoardUrl(workspaceBoard.uuid));
}
