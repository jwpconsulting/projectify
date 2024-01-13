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
import { writable } from "svelte/store";

import { goto } from "$lib/navigation";
import { getUser, updateUser } from "$lib/repository/user";
import * as userRepository from "$lib/repository/user";
import type { RepositoryContext } from "$lib/types/repository";
import type { User } from "$lib/types/user";
import { dashboardUrl } from "$lib/urls/dashboard";

export const user = writable<User | undefined>(undefined);

// TODO rename this to logIn
export async function login(
    email: string,
    password: string,
    redirectTo: string | undefined,
    repositoryContext: RepositoryContext,
): Promise<void> {
    // TODO handle result
    const response = await userRepository.logIn(
        email,
        password,
        repositoryContext,
    );
    user.set(response);

    await goto(redirectTo ?? dashboardUrl);
}

export async function logOut(repositoryContext: RepositoryContext) {
    await userRepository.logOut(repositoryContext);
    user.set(undefined);
}

export async function fetchUser(
    repositoryContext: RepositoryContext,
): Promise<User | undefined> {
    const userData = await getUser(repositoryContext);
    user.set(userData);
    return userData;
}

export async function updateUserProfile(
    preferredName: string | undefined,
    repositoryContext: RepositoryContext,
) {
    await updateUser(
        {
            preferred_name:
                preferredName === "" ? null : preferredName ?? null,
        },
        repositoryContext,
    );
    // We fetch the user to make sure the preferred name is updated
    // Ideally, this would just store the result of the above operation
    // in the user store
    await fetchUser(repositoryContext);
}
