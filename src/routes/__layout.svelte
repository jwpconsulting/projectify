<script lang="ts" context="module">
    import { browser } from "$app/env";
    import { fetchUser, user } from "$lib/stores/user";
    import routes from "$lib/routes";
    import { get } from "svelte/store";

    import "$lib/stores/global-ui";

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
            if (
                !get(user) &&
                route &&
                (route.authRequired || route.fetchUser)
            ) {
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
    import DialogModal from "$lib/components/dialogModal.svelte";
    import DatePickerDropDown from "$lib/components/datePickerDropDown.svelte";
    import ConnectionStatus from "$lib/components/connectionStatus.svelte";
    import GlobalDropDown from "$lib/components/globalDropDown.svelte";
    setClient(client);
</script>

<svelte:head>
    <title>Projectify</title>
    <meta name="description" content="Projects menagemet app" />
</svelte:head>

<slot />

<ConnectionStatus />

{#if browser}
    <DialogModal id="dataPicker">
        <DatePickerDropDown />
    </DialogModal>
{/if}

<GlobalDropDown />
