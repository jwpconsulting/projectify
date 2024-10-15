// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
import { redirect } from "@sveltejs/kit";
import type { LayoutLoadEvent } from "./$types";
import { currentUserAwaitable } from "$lib/stores/user";
import { dashboardUrl } from "$lib/urls/dashboard";
import { browser } from "$app/environment";

interface Data {
    redirectTo: string | undefined;
}

export async function load({ url }: LayoutLoadEvent): Promise<Data> {
    // TODO might want to default to dashboardUrl here with redirectTo
    const redirectTo = url.searchParams.get("next") ?? undefined;
    if (browser) {
        const user = await currentUserAwaitable();
        if (user.kind === "authenticated") {
            redirect(302, redirectTo ?? dashboardUrl);
        }
    }
    return {
        redirectTo,
    };
}

export const prerender = false;
export const ssr = false;
