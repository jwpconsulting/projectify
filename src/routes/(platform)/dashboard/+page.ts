import { redirect } from "@sveltejs/kit";

import { getDashboardWorkspaceUrl } from "$lib/urls";

import type { PageLoadEvent } from "./$types";

import { getWorkspaces } from "$lib/repository/workspace";

export const prerender = false;
export const ssr = false;

export async function load({ fetch }: PageLoadEvent): Promise<void> {
    const workspaces = await getWorkspaces({ fetch });
    if (workspaces.length === 0) {
        throw new Error("No workspaces");
    }
    const [workspace, ..._rest] = workspaces;
    // eslint-disable-next-line @typescript-eslint/no-throw-literal
    throw redirect(302, getDashboardWorkspaceUrl(workspace.uuid));
}
