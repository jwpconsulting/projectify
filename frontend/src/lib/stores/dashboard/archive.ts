// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { derived } from "svelte/store";

import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import type { ArchivedProject } from "$lib/types/workspace";
import { openApiClient } from "$lib/repository/util";

export const currentArchivedProjects = derived<
    typeof currentWorkspace,
    ArchivedProject[] | undefined
>(
    currentWorkspace,
    ($currentWorkspace, set) => {
        const uuid = $currentWorkspace.value?.uuid;
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
            .catch((error: unknown) => {
                console.error(
                    "An error happened when retrieving currentArchivedProjects",
                    { error },
                );
            });
    },
    undefined,
);
