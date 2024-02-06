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
import { redirect } from "@sveltejs/kit";

import { selectedWorkspaceBoardUuids } from "$lib/stores/dashboard";
import { getDashboardWorkspaceBoardUrl } from "$lib/urls";
import { getNewWorkspaceBoardUrl } from "$lib/urls/onboarding";

import type { PageLoadEvent } from "./$types";

export async function load({ parent }: PageLoadEvent): Promise<void> {
    // TODO call unsubscriber for selectedWorkspaceBoardUuids
    const [maybeWorkspaceBoardUuids, parentData] = await Promise.all([
        await new Promise<Map<string, string>>(
            selectedWorkspaceBoardUuids.subscribe,
        ),
        await parent(),
    ]);
    const { workspace } = parentData;

    const { uuid, workspace_boards } = workspace;

    const maybeWorkspaceBoardUuid = maybeWorkspaceBoardUuids.get(
        workspace.uuid,
    );
    if (
        maybeWorkspaceBoardUuid &&
        workspace_boards.map((b) => b.uuid).includes(maybeWorkspaceBoardUuid)
    ) {
        throw redirect(
            302,
            getDashboardWorkspaceBoardUrl(maybeWorkspaceBoardUuid),
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
