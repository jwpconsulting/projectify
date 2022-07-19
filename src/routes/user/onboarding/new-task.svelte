<script lang="ts">
    import Onboarding from "$lib/components/onboarding.svelte";
    import AppIllustration from "$lib/components/onboarding/app-illustration.svelte";
    import type { OnboardingState } from "$lib/types/onboarding";

    let workspaceTitle = "";
    let boardTitle = "";
    let taskTitle = "";
    let state: OnboardingState = "new-task";
</script>

<Onboarding
    title={"What is a task you’d like to complete?"}
    hasContentPadding={false}
    stepCount={5}
    step={2}
    viewBackButton={true}
>
    <svelte:fragment slot="prompt">
        <p>
            Tasks can be further divided into sub tasks and contain detailed
            descriptions.
        </p>
    </svelte:fragment>

    <svelte:fragment slot="inputs">
        <input
            type="text"
            name="taskTitle"
            class="input input-bordered"
            placeholder="e.g. write document"
            bind:value={taskTitle}
        />
    </svelte:fragment>

    <svelte:fragment slot="content">
        <AppIllustration {state} {workspaceTitle} {boardTitle} {taskTitle} />
    </svelte:fragment>
</Onboarding>
