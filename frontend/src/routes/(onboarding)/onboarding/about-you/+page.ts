// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2024 JWP Consulting GK
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
import type { PageLoadEvent } from "./$types";
import { getLogInWithNextUrl } from "$lib/urls/user";

export async function load({ parent, url }: PageLoadEvent) {
    const { userAwaitable } = await parent();
    const user = await userAwaitable;
    if (user.kind !== "authenticated") {
        redirect(302, getLogInWithNextUrl(url.pathname));
    }
    return { user };
}
