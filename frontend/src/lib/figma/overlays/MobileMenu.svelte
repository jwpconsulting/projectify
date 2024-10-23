<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import HeaderButton from "$lib/funabashi/buttons/HeaderButton.svelte";
    import { closeMobileMenu } from "$lib/stores/globalUi";

    $: links = [
        { label: $_("navigation.header.solutions"), href: "/solutions" },
        { label: $_("navigation.header.help"), href: "/help" },
        { label: $_("navigation.header.pricing"), href: "/pricing" },
    ];
</script>

<div class="flex flex-col">
    {#each links as link}
        <HeaderButton
            action={{
                kind: "a",
                href: link.href,
                onInteract: closeMobileMenu,
            }}
            label={link.label}
        />
    {/each}
</div>
