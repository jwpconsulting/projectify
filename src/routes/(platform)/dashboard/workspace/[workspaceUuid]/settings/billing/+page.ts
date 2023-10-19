import { getWorkspaceCustomer } from "$lib/repository/corporate";
import type { Customer } from "$lib/types/corporate";

import type { PageLoadEvent } from "./$types";

interface Data {
    customer: Customer;
}

export async function load({
    params: { workspaceUuid },
    fetch,
}: PageLoadEvent): Promise<Data> {
    const customer = await getWorkspaceCustomer(workspaceUuid, { fetch });
    return {
        customer,
    };
}
