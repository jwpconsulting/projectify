<script lang="ts" context="module">
    import { browser } from "$app/env";
    import { fetchUser } from "$lib/stores/user";
    import routes from "$lib/routes";

    export async function load({ url }) {
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
            if (route && (route.authRequired || route.fetchUser)) {
                await fetchUser();
            }
        }
        return {};
    }
</script>

<script lang="ts">
    import "../app.scss";
    import "../i18n.js";
    import { client } from "$lib/graphql/client";
    import { setClient } from "svelte-apollo";
    setClient(client);
</script>

<slot />
