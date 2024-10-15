// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { error } from "@sveltejs/kit";

import { currentWorkspaces } from "$lib/stores/dashboard/workspace";
import { currentUserAwaitable } from "$lib/stores/user";
import type { CurrentUser } from "$lib/types/user";
import { getLogInWithNextUrl } from "$lib/urls/user";

import type { LayoutLoadEvent } from "./$types";
import { goto } from "$app/navigation";

export function load({ url }: LayoutLoadEvent): {
    userAwaitable: Promise<CurrentUser>;
} {
    const userAwaitable = currentUserAwaitable();
    (async () => {
        const user = await userAwaitable;
        if (user.kind === "start") {
            error(500, "User was not loaded correctly");
        } else if (user.kind === "unauthenticated") {
            const next = getLogInWithNextUrl(url.pathname);
            console.log("Not logged in, redirecting to", next);
            await goto(next);
            return;
        } else {
            currentWorkspaces.load().catch((error: unknown) => {
                console.error("Error when loading currentWorkspaces", error);
            });
        }
    })().catch((error: unknown) => {
        console.error(
            "There was an unknown error when fetching the root user awaitable",
            error,
        );
    });
    return { userAwaitable };
}

export const ssr = false;
