<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Onboarding from "$lib/components/Onboarding.svelte";
    import { startUrl } from "$lib/urls/onboarding";

    import { page } from "$app/stores";
</script>

<Onboarding
    nextLabel={$_("onboarding.error.try-again")}
    nextAction={{ kind: "a", href: startUrl }}
>
    <svelte:fragment slot="title"
        >{$_("onboarding.error.title")}</svelte:fragment
    >
    <div class="flex flex-col gap-4" slot="prompt">
        {#if $page.error?.message}
            <h2 class="font-bold">{$_("onboarding.error.error-detail")}</h2>
            <p>{$page.error.message}</p>
        {/if}
        <p>{$_("onboarding.error.message")}</p>
    </div>
    <svelte:fragment slot="content"></svelte:fragment>
</Onboarding>
