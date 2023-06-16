import { get } from "svelte/store";
import { redirect } from "@sveltejs/kit";
import type { LayoutLoadEvent } from "./$types";
import { user } from "$lib/stores/user";

export function load({ url }: LayoutLoadEvent) {
    const currentUser = get(user);
    if (currentUser === null) {
        // eslint-disable-next-line @typescript-eslint/no-throw-literal
        throw redirect(302, `/login?next=${url.href}`);
    }
}

export const prerender = true;
