import { redirect } from "@sveltejs/kit";

import { emailConfirmation } from "$lib/stores/user";

import type { PageLoadEvent } from "./$types";

export async function load({ params: { email, token } }: PageLoadEvent) {
    await emailConfirmation(email, token);

    throw redirect(302, "/login");
}
