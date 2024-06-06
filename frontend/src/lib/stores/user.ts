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
import type { CurrentUser, User } from "$lib/types/user";
import { dataOrThrow, openApiClient } from "$lib/repository/util";
import { browser } from "$app/environment";
import { backOff } from "exponential-backoff";

const fetchUserBackOff = () =>
    backOff(() => dataOrThrow(openApiClient.GET("/user/user/current-user")));

const _user = writable<CurrentUser>({ kind: "start" }, (set) => {
    if (!browser) {
        return;
    }
    fetchUserBackOff()
        .then(({ data: user }) => {
            set(user);
        })
        .catch((error: unknown) =>
            console.error("Error when loading user", error),
        );
});
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
        _user.update(($user) => {
            return { ...$user, ...data };
        });
    } else {
        console.error(error);
    }
    return { data, error, response };
}

export async function logOut(_repositoryContext: RepositoryContext) {
    const { error, data } = await openApiClient.POST("/user/user/log-out");
    if (error) {
        throw new Error("Error when logging out");
    }
    _user.set(data);
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
