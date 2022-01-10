<script lang="ts" context="module">
    import { browser } from "$app/env";
    import { fetchUser } from "$lib/stores/user";
    import routes from "$lib/routes";

    export async function load({ url }) {
        if (browser) {
            const route = routes.find((r) => r.to === url.pathname);
            if (route && route.authRequired) {
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
    import { client } from "$lib/grapql/client";
    import { setClient } from "svelte-apollo";
    setClient(client);
</script>

<Header />
<slot />
