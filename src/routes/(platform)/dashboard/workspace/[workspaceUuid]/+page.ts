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

import { getArchivedWorkspaceBoards } from "$lib/repository/workspace/workspaceBoard";
import { selectedWorkspaceBoardUuids } from "$lib/stores/dashboard";
import { getArchiveUrl, getDashboardWorkspaceBoardUrl } from "$lib/urls";
import { getNewWorkspaceBoardUrl } from "$lib/urls/onboarding";

import type { PageLoadEvent } from "./$types";

export async function load({ parent, fetch }: PageLoadEvent): Promise<void> {
    // TODO call unsubscriber for selectedWorkspaceBoardUuids
    const [maybeWorkspaceBoardUuids, parentData] = await Promise.all([
        await new Promise<Map<string, string>>(
            // Read from localstorage what the selected ws board uuids are
            selectedWorkspaceBoardUuids.subscribe,
        ),
        await parent(),
    ]);

    const { uuid: workspaceUuid, workspace_boards } = parentData.workspace;

    // We see if the user has selected a workspace board UUID for this
    // workspace before (by referencing local storage above)
    // And if we have one ...
    const maybeWorkspaceBoardUuid =
        maybeWorkspaceBoardUuids.get(workspaceUuid);
    if (
        maybeWorkspaceBoardUuid &&
        workspace_boards.map((b) => b.uuid).includes(maybeWorkspaceBoardUuid)
    ) {
        // ... we redirect to it
        throw redirect(
            302,
            getDashboardWorkspaceBoardUrl(maybeWorkspaceBoardUuid),
        );
    }
    // If we can't find it, that's also OK, because:
    // If we find any workspace boards, we pick the first and direct the user there
    const first_workspace_board = workspace_boards.at(0);
    if (first_workspace_board) {
        const { uuid } = first_workspace_board;
        // TODO show the user a notification in case of a redirect to here
        // Indicate that the previous UUID is not available anymore
        throw redirect(302, getDashboardWorkspaceBoardUrl(uuid));
    }

    // Now we check if anything is archived and redirect to the archive in that
    // case
    const archived = await getArchivedWorkspaceBoards(workspaceUuid, {
        fetch,
    });
    if (archived && archived.length > 0) {
        // There are archived boards, so we redirect to the ws board archive
        // TODO show the user a notification in case of a redirect to here
        throw redirect(302, getArchiveUrl(workspaceUuid));
    }
    // TODO maybe throw in a nice notification to the user here that we have
    // not found any workspace board for this workspace
    throw redirect(302, getNewWorkspaceBoardUrl(workspaceUuid));
}
