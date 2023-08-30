import { redirect } from "@sveltejs/kit";
import { get } from "svelte/store";

import type { LayoutLoadEvent } from "./$types";

import { fetchUser, user } from "$lib/stores/user";
import type { User } from "$lib/types/user";

export async function load({
    url,
    fetch,
}: LayoutLoadEvent): Promise<{ user: User }> {
    const currentUser = get(user);
    if (currentUser) {
        return { user: currentUser };
    }

    const fetchedUser = await fetchUser({ fetch });

    if (fetchedUser) {
        return { user: fetchedUser };
    }

    const next = `/login?next=${url.href}`;
    console.log("Not logged in, redirecting to", next);
    throw redirect(302, next);
}

export const prerender = false;
export const ssr = false;
