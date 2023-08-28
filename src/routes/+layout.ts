import "$lib/stores/globalUi";

import "$lib/i18n";

import { locale } from "svelte-i18n";

import { browser } from "$app/environment";
import { fetchUser } from "$lib/stores/user";

export async function load({ fetch }: { fetch: typeof window.fetch }) {
    if (browser) {
        await Promise.all([
            locale.set(window.navigator.language),
            fetchUser({ fetch }),
        ]);
    }
    // TODO add waitLocale await here
    return {};
}

export const prerender = true;
