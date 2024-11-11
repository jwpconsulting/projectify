// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { redirect } from "@sveltejs/kit";

import { currentWorkspaces } from "$lib/stores/dashboard/workspace";
import type { CurrentUser } from "$lib/types/user";
import { getLogInWithNextUrl } from "$lib/urls/user";

import type { LayoutLoadEvent } from "./$types";
import { currentUser } from "$lib/stores/user";

interface Data {
    user: CurrentUser;
}

export async function load({ url }: LayoutLoadEvent): Promise<Data> {
    const user = await currentUser.load();
    console.log({ user });
    if (user.kind === "unauthenticated") {
        const next = getLogInWithNextUrl(url.pathname);
        console.log("Not logged in, redirecting to", next);
        redirect(302, next);
    }
    currentWorkspaces.load().catch((error: unknown) => {
        console.error("Error when loading currentWorkspaces", error);
    });
    return { user };
}

export const ssr = true;
export const prerender = false;
