import { redirect, error } from "@sveltejs/kit";

import { getWorkspaceBoardSection } from "$lib/repository/workspace";
import { getDashboardWorkspaceBoardUrl } from "$lib/urls";

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
    if (!workspaceBoardSection) {
        throw error(404);
    }
    const workspaceBoard = workspaceBoardSection.workspace_board;
    if (!workspaceBoard) {
        // Unlikely
        throw new Error("Expected workspaceBoard");
    }
    throw redirect(302, getDashboardWorkspaceBoardUrl(workspaceBoard.uuid));
}
