import { derived } from "svelte/store";

import { getWorkspaceCustomer } from "$lib/repository/corporate";
import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import type { Customer } from "$lib/types/corporate";

export const currentCustomer = derived<
    [typeof currentWorkspace],
    Customer | null
>(
    [currentWorkspace],
    ([$currentWorkspace], set) => {
        if (!$currentWorkspace) {
            set(null);
            return;
        }
        set(null);
        getWorkspaceCustomer($currentWorkspace.uuid)
            .then((customer) => set(customer))
            .catch((error: Error) => {
                console.error(
                    "An error happened when fetching the currentCustomer",
                    { error }
                );
            });
    },
    null
);
