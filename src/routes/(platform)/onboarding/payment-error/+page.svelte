<script lang="ts">
    import { _ } from "svelte-i18n";

    import AppIllustration from "$lib/components/onboarding/app-illustration.svelte";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import type { OnboardingState } from "$lib/types/onboarding";

    const workspaceTitle = "";
    const state: OnboardingState = "payment-error";
</script>

<Onboarding nextLabel={$_("onboarding.payment-error.continue")}>
    <svelte:fragment slot="title"
        >{$_("onboarding.payment-error.title")}</svelte:fragment
    >
    <svelte:fragment slot="prompt">
        {#each $_("onboarding.payment-error.prompt") as prompt}
            <p>{prompt}</p>
        {/each}
    </svelte:fragment>

    <svelte:fragment slot="content">
        <AppIllustration {state} {workspaceTitle} />
    </svelte:fragment>
</Onboarding>
