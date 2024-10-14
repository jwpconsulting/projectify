<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _, json } from "svelte-i18n";

    import Onboarding from "$lib/components/Onboarding.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { aboutYouUrl } from "$lib/urls/onboarding";

    $: promptLines = $json("onboarding.welcome.prompt") as string[];
</script>

<svelte:head><title>{$_("onboarding.welcome.title")}</title></svelte:head>

<Onboarding nextAction={{ kind: "a", href: aboutYouUrl }}>
    <svelte:fragment slot="title"
        >{$_("onboarding.welcome.heading")}</svelte:fragment
    >
    <svelte:fragment slot="prompt">
        {#each promptLines as promptLine}
            <p>{promptLine}</p>
        {/each}
        <Anchor
            size="large"
            href="/help/quota#quotas-for-trial-workspaces"
            label={$_("onboarding.welcome.help.trial-mode-features")}
            openBlank
        />
    </svelte:fragment>
    <svelte:fragment slot="content"></svelte:fragment>
</Onboarding>
