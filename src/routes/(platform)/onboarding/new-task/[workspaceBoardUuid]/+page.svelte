<script lang="ts">
    import { _ } from "svelte-i18n";

    import AppIllustration from "$lib/components/onboarding/app-illustration.svelte";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { goto } from "$lib/navigation";
    import {
        createTask,
        createWorkspaceBoardSection,
    } from "$lib/repository/workspace";
    import type { OnboardingState } from "$lib/types/onboarding";
    import type { CreateUpdateTask } from "$lib/types/workspace";
    import { getNewLabelUrl } from "$lib/urls/onboarding";

    import type { PageData } from "./$types";

    export let data: PageData;

    const { user, workspace, workspaceBoard, workspaceBoardSection } = data;

    const workspaceTitle = workspace.title;
    const boardTitle = workspaceBoard.title;
    let taskTitle: string | undefined = undefined;
    const state: OnboardingState = "new-task";

    $: workspaceBoardSectionTitle =
        workspaceBoardSection?.title ??
        $_("onboarding.new-task.workspace-board-section-title");

    $: disabled = taskTitle === undefined;
    // TODO use new create task function here
    async function submit() {
        if (!taskTitle) {
            throw new Error("Expected taskTitle");
        }
        const workspace_board_section = await createWorkspaceBoardSection(
            workspaceBoard,
            // TODO allow description undefined
            { title: workspaceBoardSectionTitle, description: "" }
        );
        // Find ourselves
        const assignee = workspace.workspace_users.find(
            (w) => w.user.email === user.email
        );
        // TODO get our workspaceUser instance here and then assign ourselves
        // directly
        const task: CreateUpdateTask = {
            title: taskTitle,
            labels: [],
            workspace_board_section,
            assignee,
        };
        const { uuid } = await createTask(task, { fetch });
        await goto(getNewLabelUrl(uuid));
    }
</script>

<Onboarding
    title={$_("onboarding.new-task.title")}
    hasContentPadding={false}
    stepCount={5}
    step={2}
    nextAction={{ kind: "submit", disabled, submit }}
>
    <svelte:fragment slot="prompt">
        <div class="flex flex-col gap-4">
            {#if workspaceBoardSection}
                <p>
                    {$_("onboarding.new-task.prompt.exists", {
                        values: { workspaceBoardSectionTitle },
                    })}
                </p>
            {:else}
                <p>
                    {$_("onboarding.new-task.prompt.location", {
                        values: { workspaceBoardSectionTitle },
                    })}
                </p>
            {/if}
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
