import { error } from "@sveltejs/kit";

import { getWorkspaceCustomer } from "$lib/repository/corporate";
import type { Customer } from "$lib/types/corporate";
import type { Workspace } from "$lib/types/workspace";

import type { PageLoadEvent } from "./$types";

interface Data {
    customer: Customer;
    workspace: Workspace;
}

export async function load({
    params: { workspaceUuid },
    parent,
    fetch,
}: PageLoadEvent): Promise<Data> {
    const { workspace } = await parent();
    const customer = await getWorkspaceCustomer(workspaceUuid, { fetch });
    if (!customer) {
        // TODO maybe better error message here?
        throw error(404);
    }
    return {
        customer,
        workspace,
    };
}
