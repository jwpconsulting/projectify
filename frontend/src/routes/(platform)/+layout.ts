// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023 JWP Consulting GK
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
import { redirect, error } from "@sveltejs/kit";
import { get } from "svelte/store";

import { currentWorkspaces } from "$lib/stores/dashboard";
import { currentUser } from "$lib/stores/user";
import type { User } from "$lib/types/user";
import { getLogInWithNextUrl } from "$lib/urls/user";

import type { LayoutLoadEvent } from "./$types";

export async function load({
    parent,
    url,
    fetch,
}: LayoutLoadEvent): Promise<{ user: User }> {
    const data = await parent();
    const user = get(currentUser) ?? (await data.user);
    if (user === undefined) {
        const next = getLogInWithNextUrl(url.pathname);
        console.log("Not logged in, redirecting to", next);
        redirect(302, next);
    }
    currentWorkspaces
        .load({ fetch })
        .then((workspaces) => {
            if (!workspaces) {
                error(500, "Unable to fetch workspaces");
            }
        })
        .catch((error) =>
            console.error(`Error when fetching workspaces: ${error}`),
        );

    return { user };
}
// Could we set one of the following to true here?
// Prerender: This page is completely prerenderable, there is no user data here
export const prerender = false;
// SSR, this can be prerendered
export const ssr = false;
