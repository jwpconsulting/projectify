import vars from "$lib/env";
import type { RepositoryContext } from "$lib/types/repository";
import { getCookie } from "$lib/utils/cookie";

import type { ApiResponse } from "./types";

const getOptions: RequestInit = { credentials: "include" };

function putPostOptions<T>(
    method: "POST" | "PUT" | "DELETE",
    data: T
): RequestInit {
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

async function parseResponse<T, E = unknown>(
    response: Response
): Promise<ApiResponse<T, E>> {
    const content = await response.text();
    // A response might be empty, so we can't just use await response.json()
    const data: unknown = content === "" ? undefined : JSON.parse(content);
    if (response.ok) {
        return { kind: "ok", ok: true, data: data as T };
    }
    const error: E = data as E;
    if (response.status === 400) {
        return { kind: "badRequest", ok: false, error };
    } else if (response.status === 403) {
        return { kind: "forbidden", ok: false, error };
    } else if (response.status === 404) {
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

export async function getWithCredentialsJson<T, E = unknown>(
    url: string,
    repositoryContext: RepositoryContext
): Promise<ApiResponse<T, E>> {
    const { fetch } = repositoryContext;
    const response = await fetch(`${vars.API_ENDPOINT}${url}`, getOptions);
    return await parseResponse<T, E>(response);
}

export async function postWithCredentialsJson<T, E = unknown>(
    url: string,
    data: unknown,
    repositoryContext: RepositoryContext
): Promise<ApiResponse<T, E>> {
    const { fetch } = repositoryContext;
    const response = await fetch(
        `${vars.API_ENDPOINT}${url}`,
        putPostOptions("POST", data)
    );
    return await parseResponse<T, E>(response);
}

export async function putWithCredentialsJson<T, E = unknown>(
    url: string,
    data: unknown,
    repositoryContext: RepositoryContext
): Promise<ApiResponse<T, E>> {
    const { fetch } = repositoryContext;
    const response = await fetch(
        `${vars.API_ENDPOINT}${url}`,
        putPostOptions("PUT", data)
    );
    return await parseResponse<T, E>(response);
}

export async function deleteWithCredentialsJson<T, E = unknown>(
    url: string,
    data: unknown,
    repositoryContext: RepositoryContext
): Promise<ApiResponse<T, E>> {
    const { fetch } = repositoryContext;
    const response = await fetch(
        `${vars.API_ENDPOINT}${url}`,
        putPostOptions("DELETE", data)
    );
    return await parseResponse<T, E>(response);
}

/*
 * Convenience method for callers that only care about 404 or not
 */
export function handle404<T>(result: ApiResponse<T, unknown>): T | undefined {
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
