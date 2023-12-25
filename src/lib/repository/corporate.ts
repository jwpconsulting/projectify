import {
    getWithCredentialsJson,
    handle404,
    postWithCredentialsJson,
} from "$lib/repository/util";
import type { Customer } from "$lib/types/corporate";
import type { RepositoryContext } from "$lib/types/repository";
import type { Workspace } from "$lib/types/workspace";

import type { ApiResponse } from "./types";

export async function getWorkspaceCustomer(
    // TODO accept Workspace type
    workspace_uuid: string,
    repositoryContext: RepositoryContext,
): Promise<Customer | undefined> {
    const result = await getWithCredentialsJson<Customer>(
        `/corporate/workspace/${workspace_uuid}/customer`,
        repositoryContext,
    );
    return handle404<Customer>(result);
}

interface StripeSession {
    url: string;
}

export async function createCheckoutSession(
    // TODO accept Workspace
    workspace_uuid: string,
    seats: number,
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<StripeSession, unknown>> {
    return await postWithCredentialsJson<StripeSession>(
        `/corporate/workspace/${workspace_uuid}/create-checkout-session`,
        { seats },
        repositoryContext,
    );
}

export async function createBillingPortalSession(
    workspace_uuid: string,
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<StripeSession, unknown>> {
    return await postWithCredentialsJson<StripeSession>(
        `/corporate/workspace/${workspace_uuid}/create-billing-portal-session`,
        {},
        repositoryContext,
    );
}

type ErrorContent = string | { code?: string };

export async function redeemCoupon(
    { uuid }: Pick<Workspace, "uuid">,
    code: string,
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<void, ErrorContent>> {
    return await postWithCredentialsJson(
        `/corporate/workspace/${uuid}/redeem-coupon`,
        { code },
        repositoryContext,
    );
}
