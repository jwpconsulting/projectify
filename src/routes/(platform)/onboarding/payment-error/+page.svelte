<script lang="ts">
    import { _ } from "svelte-i18n";

    import AppIllustration from "$lib/components/onboarding/app-illustration.svelte";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import type { OnboardingState } from "$lib/types/onboarding";

    let workspaceTitle = "";
    let state: OnboardingState = "payment-error";
</script>

<Onboarding
    title={$_("onboarding.payment-error.title")}
    nextLabel={$_("onboarding.payment-error.continue")}
    hasContentPadding={false}
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
