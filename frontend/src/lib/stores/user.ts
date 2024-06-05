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
import { readonly, writable } from "svelte/store";

import type { RepositoryContext } from "$lib/types/repository";
import type { User } from "$lib/types/user";
import { openApiClient } from "$lib/repository/util";

const _user = writable<User | undefined>(undefined);
export const currentUser = readonly(_user);

export async function logIn(
    email: string,
    password: string,
    _repositoryContext: RepositoryContext,
) {
    const { response, data, error } = await openApiClient.POST(
        "/user/user/log-in",
        {
            body: { email, password },
        },
    );
    if (data) {
        _user.set(data);
    } else {
        console.error(error);
    }
    return { data, error, response };
}

export async function logOut(_repositoryContext: RepositoryContext) {
    const { response } = await openApiClient.POST("/user/user/log-out");
    if (!response.ok) {
        throw new Error("Could not log out");
    }
    _user.set(undefined);
}

export async function fetchUser(): Promise<User | undefined> {
    const { response, data } = await openApiClient.GET(
        "/user/user/current-user",
    );
    if (data === undefined) {
        console.error(await response.json());
        throw new Error("Could not load user");
    }
    const userData = "unauthenticated" in data ? undefined : data;
    _user.set(userData);
    return userData;
}

export async function updateUserProfile(
    preferred_name: string | null,
): Promise<User> {
    const { data, error } = await openApiClient.PUT(
        "/user/user/current-user",
        { body: { preferred_name } },
    );
    if (error) {
        throw new Error("Expected response.ok");
    }
    _user.set(data);
    return data;
}
