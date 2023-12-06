<script lang="ts">
    import { _, json } from "svelte-i18n";

    import Onboarding from "$lib/components/Onboarding.svelte";
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
    </svelte:fragment>
    <svelte:fragment slot="content"></svelte:fragment>
</Onboarding>
