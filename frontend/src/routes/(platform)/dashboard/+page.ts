// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
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
