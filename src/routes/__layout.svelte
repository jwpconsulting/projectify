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
                    console.log(
                        url.pathname,
                        r.to,
                        url.pathname.indexOf(r.to)
                    );
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
    import Header from "$lib/components/Header.svelte";
    import "../i18n.js";
    import { client } from "$lib/graphql/client";
    import { setClient } from "svelte-apollo";
    setClient(client);
</script>

<Header />
<slot />
