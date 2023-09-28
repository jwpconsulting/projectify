import { derived } from "svelte/store";

import { getWorkspaceCustomer } from "$lib/repository/corporate";
import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import type { Customer } from "$lib/types/corporate";

export const currentCustomer = derived<typeof currentWorkspace, Customer>(
    currentWorkspace,
    ($currentWorkspace, set) => {
        const uuid = $currentWorkspace?.uuid;
        if (!uuid) {
            return;
        }
        getWorkspaceCustomer(uuid)
            .then(set)
            .catch((error: Error) => {
                console.error(
                    "An error happened when fetching the currentCustomer",
                    { error }
                );
            });
    }
);
