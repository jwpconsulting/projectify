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
import "$lib/stores/globalUi";

import "$lib/i18n";

import { locale } from "svelte-i18n";

import { fetchUser } from "$lib/stores/user";
import type { User } from "$lib/types/user";

import { browser } from "$app/environment";

interface Data {
    user?: Promise<User | undefined>;
}

export async function load({
    fetch,
}: {
    fetch: typeof window.fetch;
}): Promise<Data> {
    if (browser) {
        await Promise.all([locale.set(window.navigator.language)]);
        return { user: fetchUser({ fetch }) };
    }
    // TODO add waitLocale await here
    return {};
}

export const prerender = true;
