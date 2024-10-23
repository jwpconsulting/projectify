<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { getProfileUrl } from "$lib/urls";
</script>

<h1 class="text-center text-2xl font-bold">
    {$_("user-account-settings.update-email-address.confirmed.title")}
</h1>
<div class="flex flex-col gap-4">
    {$_("user-account-settings.update-email-address.confirmed.message")}
    <Anchor
        label={$_(
            "user-account-settings.update-email-address.confirmed.back-to-profile",
        )}
        href={getProfileUrl()}
        size="normal"
    />
</div>
