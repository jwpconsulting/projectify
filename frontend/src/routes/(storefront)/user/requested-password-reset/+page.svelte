<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023, 2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { requestPasswordResetUrl } from "$lib/urls/user";
</script>

<svelte:head>
    <title>{$_("auth.requested-password-reset.title")}</title>
</svelte:head>

<section class="flex flex-col gap-4 px-8 py-4">
    <h1 class="text-2xl font-bold">
        {$_("auth.requested-password-reset.heading")}
    </h1>
    <p>
        {$_("auth.requested-password-reset.message")}
    </p>
    <p>
        {$_("auth.requested-password-reset.troubleshooting")}
    </p>

    <Anchor
        size="normal"
        label={$_("auth.requested-password-reset.request-again")}
        href={requestPasswordResetUrl}
    />
</section>
