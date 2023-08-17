<script lang="ts">
    import AppIllustration from "$lib/components/onboarding/app-illustration.svelte";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import type { OnboardingState } from "$lib/types/onboarding";

    let workspaceTitle = "";
    let state: OnboardingState = "payment-success";
    let numberOfSeats = 1;
</script>

<Onboarding title={"Your workspace is all set up!"} hasContentPadding={false}>
    <svelte:fragment slot="prompt">
        <p>Your free 31 day trial has begun.</p>
        <p>
            Your workspace has a {numberOfSeats} seats and the billing period will
            start on year-month-day after your 31 trial period ends.
        </p>
        <p>Let’s continue by setting up your boards, tasks and users.</p>
    </svelte:fragment>

    <svelte:fragment slot="content">
        <AppIllustration {state} {workspaceTitle} />
    </svelte:fragment>
</Onboarding>
