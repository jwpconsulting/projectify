<script lang="ts">
    import Onboarding from "$lib/components/onboarding.svelte";
    import AppIllustration from "$lib/components/onboarding/app-illustration.svelte";
    import type { OnboardingState } from "$lib/types/onboarding";

    let workspaceTitle = "";
    let state: OnboardingState = "payment-error";
</script>

<Onboarding
    title={"Please finish setting up your billing account"}
    nextBtnLabel={"Return to checkout"}
    hasContentPadding={false}
>
    <svelte:fragment slot="prompt">
        <p>Your free 31 day trial has not begun yet.</p>
        <p>Your workspace does not yet have seats assigned to it.</p>
        <p>Please return to Stripe to finish the checkout process.</p>
    </svelte:fragment>

    <svelte:fragment slot="content">
        <AppIllustration {state} {workspaceTitle} />
    </svelte:fragment>
</Onboarding>
