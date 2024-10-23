// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { error, redirect } from "@sveltejs/kit";

import { currentWorkspaces } from "$lib/stores/dashboard/workspace";
import { getDashboardWorkspaceUrl } from "$lib/urls";
import { startUrl } from "$lib/urls/onboarding";

import { selectedWorkspaceUuid } from "$lib/stores/dashboard/ui";
import { browser } from "$app/environment";

export async function load(): Promise<void> {
    if (!browser) {
        return;
    }
    const maybeWorkspaceUuid: string | null = await new Promise(
        selectedWorkspaceUuid.subscribe,
    );
    if (maybeWorkspaceUuid) {
        redirect(302, getDashboardWorkspaceUrl({ uuid: maybeWorkspaceUuid }));
    }
    const workspaces = await currentWorkspaces.load();
    if (!workspaces) {
        // The workspaces endpoint not being reachable is unrecoverable
        error(500);
    }
    const workspace = workspaces[0];
    if (workspace === undefined) {
        redirect(302, startUrl);
    } else {
        redirect(302, getDashboardWorkspaceUrl(workspace));
    }
}
