import { getWithCredentialsJson } from "$lib/repository/util";
import type { Customer } from "$lib/types/corporate";
import type { RepositoryContext } from "$lib/types/repository";

export async function getWorkspaceCustomer(
    workspace_uuid: string,
    repositoryContext: RepositoryContext
): Promise<Customer> {
    return await getWithCredentialsJson<Customer>(
        `/corporate/workspace/${workspace_uuid}/customer`,
        repositoryContext
    );
}
