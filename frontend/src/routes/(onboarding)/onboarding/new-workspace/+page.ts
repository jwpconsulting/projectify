// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
import type { User } from "$lib/types/user";
import type { UserWorkspace } from "$lib/types/workspace";
import { getLogInWithNextUrl } from "$lib/urls/user";
import { redirect } from "@sveltejs/kit";

import type { PageLoadEvent } from "./$types";
import { currentWorkspaces } from "$lib/stores/dashboard/workspace";

export async function load({
    parent,
    url,
}: PageLoadEvent): Promise<{ user: User; workspace?: UserWorkspace }> {
    const { user } = await parent();
    if (user.kind !== "authenticated") {
        redirect(302, getLogInWithNextUrl(url.pathname));
    }
    const workspaces = await currentWorkspaces.load();
    const workspace = workspaces.at(0);
    return { user, workspace };
}
