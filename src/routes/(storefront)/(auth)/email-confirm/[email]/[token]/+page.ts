import { redirect } from "@sveltejs/kit";

import type { PageLoadEvent } from "./$types";

import { emailConfirmation } from "$lib/stores/user";

export async function load({ params: { email, token } }: PageLoadEvent) {
    await emailConfirmation(email, token);

    throw redirect(302, "/login");
}
