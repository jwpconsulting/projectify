import "$lib/stores/globalUi";

import { browser } from "$app/environment";

import { fetchUser } from "$lib/stores/user";

export async function load({ fetch }: { fetch: typeof window.fetch }) {
    if (browser) {
        await fetchUser({ fetch });
    }
    return {};
}

export const prerender = true;
