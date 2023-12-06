import { logOut } from "$lib/stores/user";

import type { PageLoadEvent } from "./$types";

export async function load({ fetch }: PageLoadEvent): Promise<void> {
    await logOut({ fetch });
}

// we can't log out server side
export const ssr = false;
export const prerender = false;
