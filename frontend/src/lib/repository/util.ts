// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023-2024 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
import vars from "$lib/env";
import type { RepositoryContext } from "$lib/types/repository";
import { getCookie } from "$lib/utils/cookie";
import createClient, { type Middleware } from "openapi-fetch";

import type { ApiResponse } from "./types";
import type { paths } from "$lib/types/schema";

function putPostDeleteOptions<T>(
    method: "POST" | "PUT" | "DELETE",
    data?: T,
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

const baseUrl = vars.API_ENDPOINT;

// TODO consider adding content type and accept here? Perhaps based on
// if GET or else

const csrfMiddleWare: Middleware = {
    onRequest(request: Request) {
        const csrftoken = getCookie("csrftoken");
        if (csrftoken === undefined) {
            console.warn("No csrf token found");
            return request;
        }
        request.headers.set("X-CSRFToken", csrftoken);
        return request;
    },
};

export function overrideClient(fetch: typeof global.fetch) {
    openApiClient = createClientCustom(fetch);
}

function createClientCustom(fetch?: typeof global.fetch) {
    const client = createClient<paths>({
        baseUrl,
        credentials: "include",
        fetch,
    });
    client.use(csrfMiddleWare);
    return client;
}
export let openApiClient = createClientCustom();

async function fetchResponse<T, E = unknown>(
    url: string,
    options: RequestInit,
    { fetch }: RepositoryContext,
): Promise<ApiResponse<T, E>> {
    let response: Response | undefined = undefined;
    try {
        response = await fetch(`${baseUrl}${url}`, options);
    } catch (error) {
        if (!(error instanceof Error)) {
            console.error(error);
            throw new Error("Unhandleable error");
        }
        console.error(
            "Something went wrong when making an API request:",
            error,
        );
        throw error;
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
    } else if (response.status === 429) {
        return { kind: "tooManyRequests", ok: false, error };
    } else {
        console.error(
            `Out-of-scope error encountered (status code ${response.status})`,
        );
        throw new Error(`${response.statusText}: ${JSON.stringify(data)}`);
    }
}

export async function postWithCredentialsJson<T, E = unknown>(
    url: string,
    data: unknown,
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<T, E>> {
    return await fetchResponse<T, E>(
        url,
        putPostDeleteOptions("POST", data),
        repositoryContext,
    );
}

export async function putWithCredentialsJson<T, E = unknown>(
    url: string,
    data: unknown,
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<T, E>> {
    return await fetchResponse<T, E>(
        url,
        putPostDeleteOptions("PUT", data),
        repositoryContext,
    );
}

export async function deleteWithCredentialsJson<T, E = unknown>(
    url: string,
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<T, E>> {
    return await fetchResponse<T, E>(
        url,
        putPostDeleteOptions("DELETE"),
        repositoryContext,
    );
}

/*
 * Convenience method for callers that only care about 404 or not
 */
export function failOrOk<T>(result: ApiResponse<T, unknown>): T {
    if (result.ok) {
        return result.data;
    }
    console.error("Request error:", result.error);
    throw new Error("Request failed");
}
