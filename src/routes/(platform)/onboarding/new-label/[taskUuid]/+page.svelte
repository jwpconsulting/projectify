<script lang="ts">
    import { _ } from "svelte-i18n";

    import DashboardPlaceholder from "$lib/components/onboarding/DashboardPlaceholder.svelte";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { goto } from "$lib/navigation";
    import { assignLabelToTask } from "$lib/repository/workspace";
    import { createLabel } from "$lib/repository/workspace/label";
    import { getAssignTaskUrl, getNewTaskUrl } from "$lib/urls/onboarding";

    import type { PageData } from "./$types";

    export let data: PageData;

    const { workspace, workspaceBoard, workspaceBoardSection, task } = data;

    const taskTitle = task.title;
    let labelTitle: string | undefined = undefined;

    $: disabled = !labelTitle;

    async function submit() {
        if (!labelTitle) {
            throw new Error("Expected labelTitle");
        }
        const { uuid } = await createLabel(workspace, labelTitle, 0);
        // TODO use new update task end point for this
        await assignLabelToTask(task, uuid, true);
        // TODO handle if label with this name already exists
        await goto(getAssignTaskUrl(task.uuid));
    }
</script>

<Onboarding
    hasContentPadding={false}
    stepCount={5}
    step={4}
    backAction={{ kind: "a", href: getNewTaskUrl(workspaceBoard.uuid) }}
    nextAction={{ kind: "submit", disabled, submit }}
>
    <svelte:fragment slot="title"
        >{$_("onboarding.new-label.title", {
            values: { taskTitle },
        })}</svelte:fragment
    >
    <svelte:fragment slot="prompt"
        ><p>{$_("onboarding.new-label.prompt")}</p></svelte:fragment
    >

    <svelte:fragment slot="inputs">
        <InputField
            style={{ kind: "field", inputType: "text" }}
            name="label-title"
            placeholder={$_("onboarding.new-label.placeholder")}
            bind:value={labelTitle}
        />
    </svelte:fragment>

    <DashboardPlaceholder
        slot="content"
        state={{
            kind: "new-label",
            workspace,
            workspaceBoard,
            workspaceBoardSection,
            task,
            title: labelTitle ?? $_("onboarding.new-label.default-name"),
        }}
    />
</Onboarding>
