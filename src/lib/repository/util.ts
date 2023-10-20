import vars from "$lib/env";
import type { RepositoryContext } from "$lib/types/repository";
import { getCookie } from "$lib/utils/cookie";

import type { ApiResponse, ClientError } from "./types";

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

function decodeClientError(error: unknown): ClientError {
    if (Array.isArray(error)) {
        const errors = error.flatMap((e) => (typeof e === "string" ? e : []));
        return { kind: "list", errors };
    } else if (error === null) {
        throw new Error("Error was null");
    } else if (error === undefined) {
        throw new Error("Error was undefined");
    }
    // Not exactly clean...
    return { kind: "dict", dict: error as Record<string, string> };
}

async function parseResponse<T>(response: Response): Promise<ApiResponse<T>> {
    const data: unknown = await response.json();
    if (response.ok) {
        return { kind: "ok", ok: true, data: data as T };
    }
    if (response.status === 400) {
        const error = decodeClientError(data);
        return { kind: "badRequest", ok: false, error };
    } else if (response.status === 403) {
        const error = decodeClientError(data);
        return { kind: "forbidden", ok: false, error };
    } else if (response.status === 404) {
        const error = decodeClientError(data);
        return { kind: "notFound", ok: false, error };
    } else {
        // Unrecoverable
        return {
            kind: "error",
            ok: false,
            error: new Error(
                `${response.statusText}: ${JSON.stringify(data)}`
            ),
        };
    }
}

export async function getWithCredentialsJson<T>(
    url: string,
    repositoryContext: RepositoryContext
): Promise<ApiResponse<T>> {
    const { fetch } = repositoryContext;
    const response = await fetch(`${vars.API_ENDPOINT}${url}`, getOptions);
    return await parseResponse<T>(response);
}

export async function postWithCredentialsJson<T>(
    url: string,
    data: unknown,
    repositoryContext: RepositoryContext
): Promise<ApiResponse<T>> {
    const { fetch } = repositoryContext;
    const response = await fetch(
        `${vars.API_ENDPOINT}${url}`,
        putPostOptions("POST", data)
    );
    return await parseResponse<T>(response);
}

export async function putWithCredentialsJson<T>(
    url: string,
    data: unknown,
    repositoryContext: RepositoryContext
): Promise<ApiResponse<T>> {
    const { fetch } = repositoryContext;
    const response = await fetch(
        `${vars.API_ENDPOINT}${url}`,
        putPostOptions("PUT", data)
    );
    return await parseResponse<T>(response);
}

/*
 * Convenience method for callers that only care about 404 or not
 */
export function handle404<T>(result: ApiResponse<T>): T | undefined {
    if (result.kind === "notFound") {
        return undefined;
    } else if (result.kind === "ok") {
        return result.data;
    } else if (result.kind === "badRequest") {
        console.error("Bad request:", result.error);
        throw new Error("Bad request");
    } else {
        throw new Error(`Error: ${JSON.stringify(result.error)}`);
    }
}
