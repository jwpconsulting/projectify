<script lang="ts">
    import { _ } from "svelte-i18n";

    import Onboarding from "$lib/components/onboarding.svelte";
    import AppIllustration from "$lib/components/onboarding/app-illustration.svelte";
    import type { OnboardingState } from "$lib/types/onboarding";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";

    let workspaceTitle = "";
    let boardTitle = "";
    let taskTitle = "";
    let state: OnboardingState = "new-task";
</script>

<Onboarding
    title={$_("onboarding.new-task.title")}
    hasContentPadding={false}
    stepCount={5}
    step={2}
    backAction={console.error}
>
    <svelte:fragment slot="prompt">
        <p>{$_("onboarding.new-task.prompt")}</p>
    </svelte:fragment>

    <svelte:fragment slot="inputs">
        <InputField
            style={{ kind: "field", inputType: "text" }}
            name="taskTitle"
            placeholder={$_("onboarding.new-task.task-title-placeholder")}
            bind:value={taskTitle}
        />
    </svelte:fragment>

    <svelte:fragment slot="content">
        <AppIllustration {state} {workspaceTitle} {boardTitle} {taskTitle} />
    </svelte:fragment>
</Onboarding>
