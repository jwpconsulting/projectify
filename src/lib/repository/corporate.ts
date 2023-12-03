import {
    failOrOk,
    getWithCredentialsJson,
    handle404,
    postWithCredentialsJson,
} from "$lib/repository/util";
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

interface StripeSession {
    url: string;
}

export async function createBillingPortalSession(
    workspace_uuid: string,
    repositoryContext: RepositoryContext
): Promise<StripeSession> {
    return failOrOk(
        await postWithCredentialsJson<StripeSession>(
            `/corporate/workspace/${workspace_uuid}/create-billing-portal-session`,
            {},
            repositoryContext
        )
    );
}
