<script lang="ts">
    import { _ } from "svelte-i18n";

    import DashboardPlaceholder from "$lib/components/onboarding/DashboardPlaceholder.svelte";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import { getDashboardWorkspaceBoardUrl } from "$lib/urls";

    import type { PageData } from "./$types";

    export let data: PageData;

    const {
        task,
        assignee,
        workspaceBoard,
        workspaceBoardSection,
        workspace,
        label,
    } = data;

    const taskTitle = task.title;
</script>

<Onboarding
    hasContentPadding={false}
    stepCount={5}
    step={5}
    nextLabel={$_("onboarding.assign-task.continue")}
    nextAction={{
        kind: "a",
        href: getDashboardWorkspaceBoardUrl(workspaceBoard.uuid),
    }}
>
    <svelte:fragment slot="title"
        >{$_("onboarding.assign-task.title", {
            values: { taskTitle },
        })}</svelte:fragment
    >
    <svelte:fragment slot="prompt">
        <div class="flex flex-col gap-4">
            <p>{$_("onboarding.assign-task.prompt.finished")}</p>
            <p>{$_("onboarding.assign-task.prompt.adding-workspace-users")}</p>
        </div>
    </svelte:fragment>

    <DashboardPlaceholder
        slot="content"
        state={{
            kind: "assign-task",
            task,
            label,
            workspace,
            workspaceBoard,
            workspaceBoardSection,
            assignee,
        }}
    />
</Onboarding>
