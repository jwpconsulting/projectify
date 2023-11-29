import { redirect } from "@sveltejs/kit";

import { confirmEmail } from "$lib/repository/user";
import { logInUrl } from "$lib/urls/user";

import type { PageLoadEvent } from "./$types";

export async function load({
    fetch,
    params: { email, token },
}: PageLoadEvent) {
    await confirmEmail(email, token, { fetch });

    throw redirect(302, logInUrl);
}
