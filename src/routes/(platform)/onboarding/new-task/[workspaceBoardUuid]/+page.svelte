<script lang="ts">
    import { _ } from "svelte-i18n";

    import DashboardPlaceholder from "$lib/components/onboarding/DashboardPlaceholder.svelte";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { goto } from "$lib/navigation";
    import {
        createTask,
        createWorkspaceBoardSection,
    } from "$lib/repository/workspace";
    import type { CreateUpdateTask } from "$lib/types/workspace";
    import { getNewLabelUrl } from "$lib/urls/onboarding";

    import type { PageData } from "./$types";

    export let data: PageData;

    const { user, workspace, workspaceBoard, workspaceBoardSection } = data;

    let taskTitle: string | undefined = undefined;

    $: workspaceBoardSectionTitle =
        workspaceBoardSection?.title ??
        $_("onboarding.new-task.workspace-board-section-title");

    $: disabled = taskTitle === undefined;
    async function submit() {
        if (!taskTitle) {
            throw new Error("Expected taskTitle");
        }
        const workspace_board_section = await createWorkspaceBoardSection(
            workspaceBoard,
            { title: workspaceBoardSectionTitle },
            { fetch }
        );
        // Find ourselves
        const assignee = workspace.workspace_users.find(
            (w) => w.user.email === user.email
        );
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
    hasContentPadding={false}
    stepCount={5}
    step={2}
    nextAction={{ kind: "submit", disabled, submit }}
>
    <svelte:fragment slot="title"
        >{$_("onboarding.new-task.title")}</svelte:fragment
    >
    <svelte:fragment slot="prompt">
        <div class="flex flex-col gap-4">
            <p>
                {#if workspaceBoardSection}
                    {$_("onboarding.new-task.prompt.exists", {
                        values: { workspaceBoardSectionTitle },
                    })}
                {:else}
                    {$_("onboarding.new-task.prompt.location", {
                        values: { workspaceBoardSectionTitle },
                    })}
                {/if}
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

    <DashboardPlaceholder
        slot="content"
        state={{
            kind: "new-task",
            workspace,
            workspaceBoard,
            workspaceBoardSectionTitle,
            title: taskTitle ?? $_("onboarding.new-task.default-name"),
        }}
    />
</Onboarding>
