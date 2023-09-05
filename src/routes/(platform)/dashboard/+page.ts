import { error, redirect } from "@sveltejs/kit";

import { getDashboardWorkspaceUrl } from "$lib/urls";

import type { PageLoadEvent } from "./$types";

import { getWorkspaces } from "$lib/repository/workspace";
import { selectedWorkspaceUuid } from "$lib/stores/dashboard";

export async function load({ fetch }: PageLoadEvent): Promise<void> {
    const maybeWorkspaceUuid: string | null = await new Promise(
        selectedWorkspaceUuid.subscribe
    );
    if (maybeWorkspaceUuid) {
        throw redirect(302, getDashboardWorkspaceUrl(maybeWorkspaceUuid));
    }
    const workspaces = await getWorkspaces({ fetch });
    if (workspaces.length === 0) {
        throw error(404, {
            message: "No workspaces found",
        });
    }
    const [workspace, ..._rest] = workspaces;
    throw redirect(302, getDashboardWorkspaceUrl(workspace.uuid));
}
