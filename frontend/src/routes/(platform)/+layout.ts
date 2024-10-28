// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { error, redirect } from "@sveltejs/kit";

import { currentWorkspaces } from "$lib/stores/dashboard/workspace";
import { currentUserAwaitable } from "$lib/stores/user";
import type { CurrentUser } from "$lib/types/user";
import { getLogInWithNextUrl } from "$lib/urls/user";

import type { LayoutLoadEvent } from "./$types";

interface Data {
    user: CurrentUser;
}

export async function load({ url }: LayoutLoadEvent): Promise<Data> {
    const user = await currentUserAwaitable();
    console.log({ user });
    if (user.kind === "start") {
        error(500, "User was not loaded correctly");
    } else if (user.kind === "unauthenticated") {
        const next = getLogInWithNextUrl(url.pathname);
        console.log("Not logged in, redirecting to", next);
        redirect(302, next);
    } else {
        currentWorkspaces.load().catch((error: unknown) => {
            console.error("Error when loading currentWorkspaces", error);
        });
    }
    return { user };
}

export const ssr = true;
