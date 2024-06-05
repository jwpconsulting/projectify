// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023, 2024 JWP Consulting GK
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
import { postWithCredentialsJson } from "$lib/repository/util";
import type { RepositoryContext } from "$lib/types/repository";
import type { User } from "$lib/types/user";

import type { ApiResponse } from "./types";

// Create
// Update
// Delete
// RPC
export async function confirmEmailAddressUpdate(
    confirmation_token: string,
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<void, { confirmation_token?: string }>> {
    return await postWithCredentialsJson(
        "/user/user/email-address-update/confirm",
        { confirmation_token },
        repositoryContext,
    );
}

// Auth
export async function confirmEmail(
    email: string,
    token: string,
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<unknown, unknown>> {
    return await postWithCredentialsJson(
        "/user/user/confirm-email",
        { email, token },
        repositoryContext,
    );
}

export async function logIn(
    email: string,
    password: string,
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<User, { email?: string; password?: string }>> {
    return await postWithCredentialsJson(
        "/user/user/log-in",
        { email, password },
        repositoryContext,
    );
}

export async function logOut(
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<void, void>> {
    return await postWithCredentialsJson(
        "/user/user/log-out",
        undefined,
        repositoryContext,
    );
}

export async function requestPasswordReset(
    email: string,
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<void, { email?: string }>> {
    return await postWithCredentialsJson(
        "/user/user/request-password-reset",
        { email },
        repositoryContext,
    );
}

export async function confirmPasswordReset(
    email: string,
    token: string,
    newPassword: string,
    repositoryContext: RepositoryContext,
): Promise<
    ApiResponse<
        void,
        { token?: string; email?: string; new_password?: string }
    >
> {
    return await postWithCredentialsJson(
        "/user/user/confirm-password-reset",
        { email, token, new_password: newPassword },
        repositoryContext,
    );
}
