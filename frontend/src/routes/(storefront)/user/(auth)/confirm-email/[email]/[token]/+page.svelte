<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { logInUrl } from "$lib/urls/user";

    import type { PageData } from "./$types";

    export let data: PageData;
    const { error } = data;
    const details = error?.code === 400 ? error.details : undefined;
</script>

<section class="flex flex-col gap-4 px-8 py-4">
    {#if error === undefined}
        <h1 class="text-2xl font-bold">
            {$_("auth.confirm-email.success.title")}
        </h1>
        <p>
            {$_("auth.confirm-email.success.message")}
        </p>

        <Anchor
            size="normal"
            label={$_("auth.confirm-email.success.continue")}
            href={logInUrl}
        />
    {:else if error.code === 500}
        <p>{$_("auth.confirm-email.error.try-again")}</p>
    {:else if details}
        <h1 class="text-2xl font-bold">
            {$_("auth.confirm-email.error.title")}
        </h1>
        <p>
            {$_("auth.confirm-email.error.message")}
        </p>
        {#if details.email !== undefined}
            <p>
                {$_("auth.confirm-email.error.email", {
                    values: { error: details.email },
                })}
            </p>
        {/if}
        {#if details.token}
            <p>
                {$_("auth.confirm-email.error.token", {
                    values: { error: details.token },
                })}
            </p>
        {/if}
        <Anchor
            size="normal"
            label={$_("auth.confirm-email.error.continue")}
            href="/contact-us"
        />
    {/if}
</section>
