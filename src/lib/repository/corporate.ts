import { getWithCredentialsJson, handle404 } from "$lib/repository/util";
import type { Customer } from "$lib/types/corporate";
import type { RepositoryContext } from "$lib/types/repository";

export async function getWorkspaceCustomer(
    workspace_uuid: string,
    repositoryContext: RepositoryContext
): Promise<Customer | undefined> {
    const result = await getWithCredentialsJson<Customer>(
        `/corporate/workspace/${workspace_uuid}/customer`,
        repositoryContext
    );
    return handle404<Customer>(result);
}
