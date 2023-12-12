import vars from "$lib/env";
import type { RepositoryContext } from "$lib/types/repository";
import { getCookie } from "$lib/utils/cookie";

import type { ApiResponse } from "./types";

const getOptions: RequestInit = {
    credentials: "include",
    headers: {
        Accept: "application/json",
    },
};

function putPostDeleteOptions<T>(
    method: "POST" | "PUT" | "DELETE",
    data?: T
): RequestInit {
    // These requests will certainly fail without a csrf token
    // XXX or will they? Seems like we generously disabled CSRF checking
    // hehehe...
    const csrftoken = getCookie("csrftoken");
    return {
        method,
        // TODO serialize using new FormData()
        body: data === undefined ? undefined : JSON.stringify(data),
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
            ...(csrftoken ? { "X-CSRFToken": csrftoken } : undefined),
        },
    };
}

/*
 * Carefully parse a DRF response, keeping in mind that not JSON, but a plain
 * string might be returned.
 */
function parseResponseData(data: string): unknown | string | undefined {
    if (data === "") {
        return undefined;
    }
    try {
        return JSON.parse(data) as unknown;
    } catch {
        return data;
    }
}

async function fetchResponse<T, E = unknown>(
    url: string,
    options: RequestInit,
    { fetch }: RepositoryContext
): Promise<ApiResponse<T, E>> {
    let response: Response | undefined = undefined;
    try {
        response = await fetch(`${vars.API_ENDPOINT}${url}`, options);
    } catch (error) {
        if (!(error instanceof Error)) {
            console.error(error);
            throw new Error("Unhandleable error");
        }
        console.error(
            "Something went wrong when making an API request:",
            error
        );
        return { kind: "error", ok: false, error };
    }
    const content = await response.text();
    // TODO
    // Not very clean, we still don't correctly handle DRF just returning
    // a string -- here we might reconfigure DRF to always return JSON,
    // even when erroring
    const data: unknown = parseResponseData(content);
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
    return await fetchResponse<T, E>(url, getOptions, repositoryContext);
}

export async function postWithCredentialsJson<T, E = unknown>(
    url: string,
    data: unknown,
    repositoryContext: RepositoryContext
): Promise<ApiResponse<T, E>> {
    return await fetchResponse<T, E>(
        url,
        putPostDeleteOptions("POST", data),
        repositoryContext
    );
}

export async function putWithCredentialsJson<T, E = unknown>(
    url: string,
    data: unknown,
    repositoryContext: RepositoryContext
): Promise<ApiResponse<T, E>> {
    return await fetchResponse<T, E>(
        url,
        putPostDeleteOptions("PUT", data),
        repositoryContext
    );
}

export async function deleteWithCredentialsJson<T, E = unknown>(
    url: string,
    repositoryContext: RepositoryContext
): Promise<ApiResponse<T, E>> {
    return await fetchResponse<T, E>(
        url,
        putPostDeleteOptions("DELETE"),
        repositoryContext
    );
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

export function failOrOk<T>(result: ApiResponse<T, unknown>): T {
    if (result.ok) {
        return result.data;
    }
    console.error("Request error:", result.error);
    throw new Error("Request failed");
}
