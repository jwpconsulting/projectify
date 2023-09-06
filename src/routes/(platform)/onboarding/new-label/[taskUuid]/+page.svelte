<script lang="ts">
    import { _ } from "svelte-i18n";

    import { goto } from "$lib/navigation";

    import type { PageData } from "./$types";

    import AppIllustration from "$lib/components/onboarding/app-illustration.svelte";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { assignLabelToTask, createLabel } from "$lib/repository/workspace";
    import type { OnboardingState } from "$lib/types/onboarding";
    import { getAssignTaskUrl } from "$lib/urls/onboarding";

    export let data: PageData;

    const { workspace, workspaceBoard, task } = data;

    const workspaceTitle = workspace.title;
    const boardTitle = workspaceBoard.title;
    const taskTitle = task.title;
    let labelTitle: string | undefined = undefined;
    const state: OnboardingState = "new-label";

    async function action() {
        if (!labelTitle) {
            throw new Error("Expected labelTitle");
        }
        const { uuid } = await createLabel(workspace, labelTitle, 0);
        await assignLabelToTask(task, uuid, true);
        // TODO handle if label with this name already exists
        await goto(getAssignTaskUrl(task.uuid));
    }
</script>

<Onboarding
    title={$_("onboarding.new-label.title", { values: { taskTitle } })}
    hasContentPadding={false}
    stepCount={5}
    step={4}
    backAction={console.error}
    nextAction={{ kind: "button", action }}
>
    <svelte:fragment slot="prompt">
        <p>{$_("onboarding.new-label.prompt")}</p>
    </svelte:fragment>

    <svelte:fragment slot="inputs">
        <InputField
            style={{ kind: "field", inputType: "text" }}
            name="label-title"
            placeholder={$_("onboarding.new-label.placeholder")}
            bind:value={labelTitle}
        />
    </svelte:fragment>

    <svelte:fragment slot="content">
        <AppIllustration
            {state}
            {workspaceTitle}
            {boardTitle}
            {taskTitle}
            labelName={labelTitle}
        />
    </svelte:fragment>
</Onboarding>
