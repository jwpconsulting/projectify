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

import { selectedProjectUuids } from "$lib/stores/dashboard/ui";
import { getArchiveUrl, getDashboardProjectUrl } from "$lib/urls";
import { getNewProjectUrl } from "$lib/urls/onboarding";

import type { PageLoadEvent } from "./$types";
import { openApiClient } from "$lib/repository/util";

export async function load({ parent }: PageLoadEvent): Promise<void> {
    // TODO call unsubscriber for selectedProjectUuids
    const [maybeProjectUuids, parentData] = await Promise.all([
        await new Promise<Map<string, string>>(
            // Read from localstorage what the selected ws board uuids are
            selectedProjectUuids.subscribe,
        ),
        await parent(),
    ]);

    const { uuid: workspace_uuid, projects } = parentData.workspace;

    // We see if the user has selected a project UUID for this
    // workspace before (by referencing local storage above)
    // And if we have one ...
    const maybeProjectUuid = maybeProjectUuids.get(workspace_uuid);
    if (
        maybeProjectUuid &&
        projects.map((b) => b.uuid).includes(maybeProjectUuid)
    ) {
        // ... we redirect to it
        redirect(302, getDashboardProjectUrl({ uuid: maybeProjectUuid }));
    }
    // If we can't find it, that's also OK, because:
    // If we find any projects, we pick the first and direct the user there
    const first_project = projects.at(0);
    if (first_project) {
        // TODO show the user a notification in case of a redirect to here
        // Indicate that the previous UUID is not available anymore
        redirect(302, getDashboardProjectUrl(first_project));
    }

    // Now we check if anything is archived and redirect to the archive in that
    // case
    const { data: archived } = await openApiClient.GET(
        "/workspace/workspace/{workspace_uuid}/archived-projects/",
        { params: { path: { workspace_uuid } } },
    );
    if (archived && archived.length > 0) {
        // There are archived boards, so we redirect to the ws board archive
        // TODO show the user a notification in case of a redirect to here
        redirect(302, getArchiveUrl(parentData.workspace));
    }
    // TODO maybe throw in a nice notification to the user here that we have
    // not found any project for this workspace
    redirect(302, getNewProjectUrl(workspace_uuid));
}
