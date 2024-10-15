// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { derived, type Readable } from "svelte/store";

import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import type { Customer } from "$lib/types/corporate";
import { openApiClient } from "$lib/repository/util";

type CurrentCustomer = Readable<Customer | undefined>;

export const currentCustomer: CurrentCustomer = derived<
    typeof currentWorkspace,
    Customer | undefined
>(currentWorkspace, ($currentWorkspace, set) => {
    const uuid = $currentWorkspace.value?.uuid;
    if (!uuid) {
        return;
    }
    // Hopefully this won't be run server-side, fetch is not available
    // there
    openApiClient
        .GET("/corporate/workspace/{workspace_uuid}/customer", {
            params: { path: { workspace_uuid: uuid } },
        })
        .then(({ error, data }) => {
            if (error?.code === 404) {
                throw new Error("Could not find customer");
            }
            if (data === undefined) {
                throw new Error("An error happened while geting customer");
            }
            set(data);
        })
        .catch((error: unknown) => {
            console.error(
                "An error happened when fetching the currentCustomer",
                { error },
            );
        });
});
