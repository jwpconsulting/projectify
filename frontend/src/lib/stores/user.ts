// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
import { writable } from "svelte/store";

import type { CurrentUser } from "$lib/types/user";
import { dataOrThrow, openApiClient } from "$lib/repository/util";
import { backOff } from "exponential-backoff";
import { currentWorkspaces } from "./dashboard/workspace";

const fetchUserBackOff = () =>
    backOff(() => dataOrThrow(openApiClient.GET("/user/user/current-user")));

const _user = writable<CurrentUser>({ kind: "start" });
export const currentUser = {
    subscribe: _user.subscribe,
    async load() {
        const { data } = await fetchUserBackOff();
        if (data.kind === "unauthenticated") {
            _user.set({ kind: "start" });
        } else {
            _user.set(data);
        }
        return data;
    },
};

export async function logIn(email: string, password: string) {
    const { data, error } = await openApiClient.POST("/user/user/log-in", {
        body: { email, password },
    });
    if (data) {
        _user.update(($user) => {
            return { ...$user, ...data };
        });
    }
    return { data, error };
}

async function _logOut() {
    const promise = openApiClient.POST("/user/user/log-out");
    const { data, error } = await promise;
    if (error?.code === 403) {
        return { error, data: undefined };
    }
    if (error) {
        throw new Error("Couldn't log out");
    }
    return { data, error: undefined };
}

export async function logOut() {
    const { data, error } = await backOff(_logOut);
    // In the future we'd like want to test for 401 here
    if (data) {
        _user.set(data);
    }
    currentWorkspaces.reset();
    return { data, error };
}

export async function updateUserProfile(preferred_name: string | null) {
    const { data, error } = await openApiClient.PUT(
        "/user/user/current-user/update",
        { body: { preferred_name } },
    );
    if (data) {
        _user.set(data);
        return { data };
    }
    return { error };
}
