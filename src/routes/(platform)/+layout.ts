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
import { redirect } from "@sveltejs/kit";
import { get } from "svelte/store";

import { fetchUser, user } from "$lib/stores/user";
import type { User } from "$lib/types/user";
import { getLogInWithNextUrl } from "$lib/urls/user";

import type { LayoutLoadEvent } from "./$types";

export async function load({
    url,
    fetch,
}: LayoutLoadEvent): Promise<{ user: User }> {
    // For reasons, fetchuser fires twice.
    // We should have user contain some kind of hint that the user is now
    // being fetched, so we don't fetch it twice.
    const currentUser = get(user);
    if (currentUser) {
        return { user: currentUser };
    }

    const fetchedUser = await fetchUser({ fetch });

    if (fetchedUser) {
        return { user: fetchedUser };
    }

    const next = getLogInWithNextUrl(url.href);
    console.log("Not logged in, redirecting to", next);
    throw redirect(302, next);
}
// Could we set one of the following to true here?
// Prerender: This page is completely prerenderable, there is no user data here
export const prerender = false;
// SSR, this can be prerendered
export const ssr = false;
