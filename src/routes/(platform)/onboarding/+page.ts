import { redirect } from "@sveltejs/kit";

import { startUrl } from "$lib/urls/onboarding";

export function load() {
    const redirectUrl = startUrl;
    throw redirect(302, redirectUrl);
}
