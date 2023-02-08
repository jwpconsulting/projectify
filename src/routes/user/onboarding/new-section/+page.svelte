<script lang="ts">
    import Onboarding from "$lib/components/onboarding.svelte";
    import AppIllustration from "$lib/components/onboarding/app-illustration.svelte";
    import type { OnboardingState } from "$lib/types/onboarding";

    let workspaceTitle = "";
    let boardTitle = "";
    let taskTitle = "";
    let state: OnboardingState = "new-section";
</script>

<Onboarding
    title={"We’ve put your task in a ‘To do’ section."}
    hasContentPadding={false}
    stepCount={5}
    step={3}
    viewBackButton={true}
>
    <svelte:fragment slot="prompt">
        <p>Add new sections and customise your section names.</p>
    </svelte:fragment>

    <svelte:fragment slot="content">
        <AppIllustration {state} {workspaceTitle} {boardTitle} {taskTitle} />
    </svelte:fragment>
</Onboarding>
