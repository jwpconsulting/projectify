import { redirect } from "@sveltejs/kit";

import { getDashboardWorkspaceBoardUrl } from "$lib/urls";

import type { PageLoadEvent } from "./$types";

import { selectedWorkspaceBoardUuids } from "$lib/stores/dashboard";
import { getNewWorkspaceBoardUrl } from "$lib/urls/onboarding";

export async function load({ parent }: PageLoadEvent): Promise<void> {
    const [maybeWorkspaceBoardUuids, parentData] = await Promise.all([
        await new Promise<Map<string, string>>(
            selectedWorkspaceBoardUuids.subscribe
        ),
        await parent(),
    ]);
    const { workspace } = parentData;

    const { uuid, workspace_boards } = workspace;

    if (!workspace_boards) {
        throw new Error("Expected workspace_boards");
    }

    const maybeWorkspaceBoardUuid = maybeWorkspaceBoardUuids.get(
        workspace.uuid
    );
    if (
        maybeWorkspaceBoardUuid &&
        workspace_boards.map((b) => b.uuid).includes(maybeWorkspaceBoardUuid)
    ) {
        throw redirect(
            302,
            getDashboardWorkspaceBoardUrl(maybeWorkspaceBoardUuid)
        );
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
