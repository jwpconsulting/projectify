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

import { currentWorkspaces } from "$lib/stores/dashboard/workspace";
import { currentUser } from "$lib/stores/user";
import type { CurrentUser, User } from "$lib/types/user";
import { getLogInWithNextUrl } from "$lib/urls/user";

import type { LayoutLoadEvent } from "./$types";

export async function load({
    url,
    fetch,
}: LayoutLoadEvent): Promise<{ user: User }> {
    const user: CurrentUser = await new Promise((resolve) => {
        currentUser.subscribe((user) => {
            if (user.kind === "start") {
                return;
            }
            resolve(user);
        });
    });
    if (user.kind === "start") {
        error(500, "User was not loaded correctly");
    } else if (user.kind === "unauthenticated") {
        const next = getLogInWithNextUrl(url.pathname);
        console.log("Not logged in, redirecting to", next);
        redirect(302, next);
    } else {
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
}
// Could we set one of the following to true here?
// Prerender: This page is completely prerenderable, there is no user data here
export const prerender = false;
// SSR, this can be prerendered
// TODO this can be turned to true
// Justus 2024-04-26
export const ssr = false;
