import { redirect } from "@sveltejs/kit";

import type { PageLoadEvent } from "./$types";

import { emailConfirmation } from "$lib/stores/user";

export const prerender = false;
export const ssr = false;

export async function load({ params: { email, token } }: PageLoadEvent) {
    await emailConfirmation(email, token);

    // eslint-disable-next-line @typescript-eslint/no-throw-literal
    throw redirect(302, "/login");
}
