<script lang="ts">
    import Onboarding from "$lib/components/onboarding.svelte";
    import AppIllustration from "$lib/components/onboarding/app-illustration.svelte";
    import type { OnboardingState } from "$lib/types/onboarding";

    let workspaceTitle = "";
    let boardTitle = "";
    let taskTitle = "";
    let labelName = "";
    let state: OnboardingState = "new-label";
</script>

<Onboarding
    title={`Create a label for ${taskTitle}`}
    hasContentPadding={false}
    stepCount={5}
    step={4}
    viewBackButton={true}
>
    <svelte:fragment slot="prompt">
        <p>Labels help you to filter between the types of tasks.</p>
    </svelte:fragment>

    <svelte:fragment slot="inputs">
        <input
            type="text"
            name="labelName"
            class="input input-bordered"
            placeholder="e.g. bug"
            bind:value={labelName}
        />
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
