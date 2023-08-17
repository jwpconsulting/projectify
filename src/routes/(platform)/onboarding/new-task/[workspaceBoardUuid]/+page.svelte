<script lang="ts">
    import { _ } from "svelte-i18n";

    import { goto } from "$lib/navigation";

    import type { PageData } from "./$types";

    import AppIllustration from "$lib/components/onboarding/app-illustration.svelte";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import {
        assignUserToTask,
        createTask,
        createWorkspaceBoardSection,
    } from "$lib/repository/workspace";
    import type { OnboardingState } from "$lib/types/onboarding";
    import type { CreateTask } from "$lib/types/workspace";
    import { getNewLabelUrl } from "$lib/urls/onboarding";

    export let data: PageData;

    const { user, workspace, workspaceBoard } = data;

    let workspaceTitle = workspace.title;
    let boardTitle = workspaceBoard.title;
    let taskTitle = "";
    let state: OnboardingState = "new-task";

    $: workspaceBoardSectionTitle = $_(
        "onboarding.new-task.workspace-board-section-title"
    );

    async function action() {
        const workspaceBoardSection = await createWorkspaceBoardSection(
            workspaceBoard,
            {
                title: "To Do",
                description: "",
            }
        );
        const task: CreateTask = {
            title: taskTitle,
            description: "",
            labels: [],
            // TODO deadline should be optional
            deadline: null,
            workspace_board_section: workspaceBoardSection,
        };
        const { uuid } = await createTask(task);
        await assignUserToTask(user.email, uuid);
        await goto(getNewLabelUrl(uuid));
    }
</script>

<Onboarding
    title={$_("onboarding.new-task.title")}
    hasContentPadding={false}
    stepCount={5}
    step={2}
    backAction={console.error}
    nextAction={{ kind: "button", action }}
>
    <svelte:fragment slot="prompt">
        <div class="flex flex-col gap-4">
            <p>
                {$_("onboarding.new-task.prompt.location", {
                    values: { workspaceBoardSectionTitle },
                })}
            </p>
            <p>{$_("onboarding.new-task.prompt.explanation")}</p>
        </div>
    </svelte:fragment>

    <svelte:fragment slot="inputs">
        <InputField
            style={{ kind: "field", inputType: "text" }}
            name="task-title"
            placeholder={$_("onboarding.new-task.placeholder")}
            bind:value={taskTitle}
        />
    </svelte:fragment>

    <svelte:fragment slot="content">
        <AppIllustration {state} {workspaceTitle} {boardTitle} {taskTitle} />
    </svelte:fragment>
</Onboarding>
