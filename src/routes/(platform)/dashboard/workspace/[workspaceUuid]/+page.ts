import { redirect } from "@sveltejs/kit";

import { getDashboardWorkspaceBoardUrl } from "$lib/urls";

import type { PageLoadEvent } from "./$types";

import { getWorkspace } from "$lib/repository/workspace";
import type { Workspace } from "$lib/types/workspace";
import { getNewWorkspaceBoardUrl } from "$lib/urls/onboarding";

export const prerender = false;
export const ssr = false;

export async function load({
    params: { workspaceUuid },
    fetch,
}: PageLoadEvent): Promise<void> {
    const workspace: Workspace = await getWorkspace(workspaceUuid, {
        fetch,
    });

    const { uuid, workspace_boards } = workspace;

    if (!workspace_boards) {
        throw new Error("Expected workspace_boards");
    }
    const first_workspace_board = workspace_boards.at(0);
    if (first_workspace_board) {
        const { uuid } = first_workspace_board;
        throw redirect(302, getDashboardWorkspaceBoardUrl(uuid));
    }
    // TODO maybe throw in a nice notification to the user here that we have
    // not found any workspace board for this workspace
    throw redirect(302, getNewWorkspaceBoardUrl(uuid));
}
