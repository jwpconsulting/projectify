<script lang="ts">
    import { _ } from "svelte-i18n";

    import { getDashboardWorkspaceBoardUrl } from "$lib/urls";

    import type { PageData } from "./$types";

    import AppIllustration from "$lib/components/onboarding/app-illustration.svelte";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import type { OnboardingState } from "$lib/types/onboarding";

    export let data: PageData;

    const { task, workspaceBoard, workspace, label } = data;

    const workspaceTitle = workspace.title;
    const boardTitle = workspaceBoard.title;
    const taskTitle = task.title;
    const labelName = label.name;
    const state: OnboardingState = "assign-task";
</script>

<Onboarding
    title={$_("onboarding.assign-task.title", { values: { taskTitle } })}
    hasContentPadding={false}
    stepCount={5}
    step={5}
    nextLabel={$_("onboarding.assign-task.continue")}
    backAction={console.error}
    nextAction={{
        kind: "a",
        href: getDashboardWorkspaceBoardUrl(workspaceBoard.uuid),
    }}
>
    <svelte:fragment slot="prompt">
        <div class="flex flex-col gap-4">
            <p>{$_("onboarding.assign-task.prompt.finished")}</p>
            <p>{$_("onboarding.assign-task.prompt.adding-members")}</p>
        </div>
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
