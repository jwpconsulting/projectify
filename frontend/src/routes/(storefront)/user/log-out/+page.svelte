<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { backToHomeUrl } from "$lib/urls";
    import { logInUrl } from "$lib/urls/user";
    import type { PageData } from "./$types";

    export let data: PageData;

    const { result } = data;
</script>

<svelte:head><title>{$_("auth.logout.title")}</title></svelte:head>

<div class="flex flex-col gap-8 px-8 py-8">
    <h1 class="text-center text-xl font-bold">
        {#if result === "not-browser"}
            {$_("auth.logout.logging-out")}
        {:else}
            {#await result}
                {$_("auth.logout.logging-out")}
            {:then result}
                {#if result.data}
                    {$_("auth.logout.success")}
                {:else if result.error}
                    {$_("auth.logout.already-logged-out")}
                {/if}
            {:catch}
                {$_("auth.logout.error")}
            {/await}
        {/if}
    </h1>

    <p>
        <Anchor
            size="normal"
            label={$_("auth.logout.log-back-in")}
            href={logInUrl}
        />
    </p>
    <p>
        <Anchor
            size="normal"
            label={$_("auth.logout.landing")}
            href={backToHomeUrl}
        />
    </p>
</div>
