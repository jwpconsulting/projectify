<script lang="ts">
    import { _ } from "svelte-i18n";

    import Onboarding from "$lib/components/Onboarding.svelte";
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
    nextLabel={$_("onboarding.assign-task.continue")}
    backAction={console.error}
>
    <svelte:fragment slot="prompt">
        <p>{$_("onboarding.assign-task.prompt.paragraph1")}</p>
        <p>{$_("onboarding.assign-task.prompt.paragraph2")}</p>
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
