<script lang="ts">
    import Onboarding from "$lib/components/onboarding.svelte";
    import AppIllustration from "$lib/components/onboarding/app-illustration.svelte";
    import type { OnboardingState } from "$lib/types/onboarding";

    let workspaceTitle = "";
    let boardTitle = "";
    let taskTitle = "";
    let labelName = "";
    let state: OnboardingState = "assign-task";
</script>

<Onboarding
    title={`Task ${taskTitle} has been assigned to you!`}
    hasContentPadding={false}
    stepCount={5}
    step={5}
    nextBtnLabel={"Get started"}
    viewBackButton={true}
>
    <svelte:fragment slot="prompt">
        <p>You’re all set!</p>
        <p>
            If you wish to add new members to your workspace, please go to the
            workspace settings menu next to your workspace name.
        </p>
    </svelte:fragment>

    <svelte:fragment slot="content">
        <AppIllustration
            {state}
            {workspaceTitle}
            {boardTitle}
            {taskTitle}
            {labelName}
        />
    </svelte:fragment>
</Onboarding>
