<script lang="ts">
    import { _, json } from "svelte-i18n";

    import Onboarding from "$lib/components/Onboarding.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { aboutYouUrl } from "$lib/urls/onboarding";

    $: promptLines = $json("onboarding.welcome.prompt") as string[];
</script>

<Onboarding nextAction={{ kind: "a", href: aboutYouUrl }}>
    <svelte:fragment slot="title"
        >{$_("onboarding.welcome.title")}</svelte:fragment
    >
    <svelte:fragment slot="prompt">
        {#each promptLines as promptLine}
            <p>{promptLine}</p>
        {/each}
        <Anchor
            size="large"
            href="/pricing#trial-mode"
            label={$_("onboarding.welcome.help.trial-mode-features")}
        />
    </svelte:fragment>
    <svelte:fragment slot="content"></svelte:fragment>
</Onboarding>
