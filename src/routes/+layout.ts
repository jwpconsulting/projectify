import "$lib/stores/global-ui";

import { get } from "svelte/store";

import { browser } from "$app/environment";

import { fetchUser, user } from "$lib/stores/user";
import routes from "$lib/routes";

export async function load({ url }: { url: URL }) {
    if (browser) {
        const route = routes.find((r) => {
            if (r.to === url.pathname) {
                return true;
            }

            if (url.pathname.indexOf(r.to + "/") == 0) {
                return true;
            }

            return false;
        });
        // TODO replace with store subscription
        if (!get(user) && route && (route.authRequired || route.fetchUser)) {
            await fetchUser();
        }
    }
    return {};
}
