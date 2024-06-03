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
import { derived } from "svelte/store";

import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import type { Project } from "$lib/types/workspace";
import { openApiClient } from "$lib/repository/util";

export const currentArchivedProjects = derived<
    typeof currentWorkspace,
    Project[] | undefined
>(
    currentWorkspace,
    ($currentWorkspace, set) => {
        const uuid = $currentWorkspace?.uuid;
        if (!uuid) {
            set(undefined);
            return;
        }
        // XXX this will not use { fetch } present in load() function
        // Justus 2024-04-08
        openApiClient
            .GET("/workspace/workspace/{workspace_uuid}/archived-projects/", {
                params: { path: { workspace_uuid: uuid } },
            })
            .then(({ data, error }) => {
                if (data === undefined) {
                    throw new Error(
                        `No result, error: ${JSON.stringify(error)}`,
                    );
                }
                set(data);
            })
            .catch((error: Error) => {
                console.error(
                    "An error happened when retrieving currentArchivedProjects",
                    { error },
                );
            });
    },
    undefined,
);
