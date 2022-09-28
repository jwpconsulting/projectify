import { getWithCredentialsJson } from "$lib/repository/util";
import type { Customer } from "$lib/types";

export async function getWorkspaceCustomer(
    workspace_uuid: string
): Promise<Customer> {
    return await getWithCredentialsJson<Customer>(
        `/corporate/workspace/${workspace_uuid}/customer`
    );
}
