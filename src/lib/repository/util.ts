import vars from "$lib/env";
import type { RepositoryContext } from "$lib/types/repository";
import { getCookie } from "$lib/utils/cookie";

const getOptions: RequestInit = { credentials: "include" };

function putPostOptions<T>(method: "POST" | "PUT", data: T): RequestInit {
    // These requests will certainly fail without a csrf token
    const baseHeaders = { "Content-Type": "application/json" };
    const csrftoken = getCookie("csrftoken");
    return {
        method,
        // TODO serialize using new FormData()
        body: JSON.stringify(data),
        credentials: "include",
        headers: csrftoken
            ? { ...baseHeaders, "X-CSRFToken": csrftoken }
            : baseHeaders,
    };
}

async function parseResponse<T>(response: Response): Promise<T> {
    const body = (await response.json()) as T;
    if (!response.ok) {
        throw new Error(`${response.statusText}: ${JSON.stringify(body)}`);
    }
    return body;
}

export async function getWithCredentialsJson<T>(
    url: string,
    repositoryContext: RepositoryContext
): Promise<T> {
    const { fetch } = repositoryContext;
    const response = await fetch(`${vars.API_ENDPOINT}${url}`, getOptions);
    return await parseResponse(response);
}

export async function postWithCredentialsJson<T>(
    url: string,
    data: unknown,
    repositoryContext: RepositoryContext
): Promise<T> {
    const { fetch } = repositoryContext;
    const response = await fetch(
        `${vars.API_ENDPOINT}${url}`,
        putPostOptions("POST", data)
    );
    return await parseResponse(response);
}

export async function putWithCredentialsJson<T>(
    url: string,
    data: unknown,
    repositoryContext: RepositoryContext
): Promise<T> {
    const { fetch } = repositoryContext;
    const response = await fetch(
        `${vars.API_ENDPOINT}${url}`,
        putPostOptions("PUT", data)
    );
    return await parseResponse(response);
}
