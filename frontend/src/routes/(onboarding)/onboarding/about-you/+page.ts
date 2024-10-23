// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK
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
