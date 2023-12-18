import { derived, type Readable } from "svelte/store";

import { getWorkspaceCustomer } from "$lib/repository/corporate";
import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import type { Customer } from "$lib/types/corporate";

type CurrentCustomer = Readable<Customer | undefined>;

export const currentCustomer: CurrentCustomer = derived<
    typeof currentWorkspace,
    Customer | undefined
>(currentWorkspace, ($currentWorkspace, set) => {
    const uuid = $currentWorkspace?.uuid;
    if (!uuid) {
        return;
    }
    // Hopefully this won't be run server-side, fetch is not available
    // there
    getWorkspaceCustomer(uuid, { fetch })
        .then(set)
        .catch((error: Error) => {
            console.error(
                "An error happened when fetching the currentCustomer",
                { error },
            );
        });
});
