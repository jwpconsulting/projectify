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
import { getCookie } from "$lib/utils/cookie";
import createClient, { type Middleware } from "openapi-fetch";

import type { paths } from "$lib/types/schema";

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
