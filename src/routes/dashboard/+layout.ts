import { get } from "svelte/store";
import { redirect } from "@sveltejs/kit";

import type { LayoutLoadEvent } from "./$types";

import { fetchUser, user } from "$lib/stores/user";

export async function load({ url, fetch }: LayoutLoadEvent) {
    const currentUser = get(user);
    // TODO could be refactored
    if (currentUser === null) {
        const user = await fetchUser({ fetch });
        if (user === null) {
            const next = `/login?next=${url.href}`;
            console.log("Not logged in, redirecting to", next);
            // eslint-disable-next-line @typescript-eslint/no-throw-literal
            throw redirect(302, next);
        }
    }
}

export const prerender = true;
