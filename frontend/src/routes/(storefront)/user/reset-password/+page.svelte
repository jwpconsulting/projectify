<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { logInUrl } from "$lib/urls/user";
</script>

<svelte:head>
    <title>{$_("auth.reset-password.title")}</title>
</svelte:head>

<section class="flex flex-col gap-4 px-8 py-4">
    <h1 class="text-2xl font-bold">
        {$_("auth.reset-password.heading")}
    </h1>
    <p>
        {$_("auth.reset-password.message")}
    </p>

    <Anchor
        size="normal"
        label={$_("auth.reset-password.continue")}
        href={logInUrl}
    />
</section>
