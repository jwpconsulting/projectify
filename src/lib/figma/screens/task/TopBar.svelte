<script lang="ts">
    import { _ } from "svelte-i18n";

    import Button from "$lib/figma/buttons/Button.svelte";
    import CircleIcon from "$lib/figma/buttons/CircleIcon.svelte";
    import SquovalIcon from "$lib/figma/buttons/SquovalIcon.svelte";

    import type { TaskOrNewTask, BreadCrumbTask } from "$lib/types/ui";
    import {
        isBreadCrumbWorkspaceBoardSection,
        isBreadCrumbTask,
    } from "$lib/types/ui";
    import { getDashboardWorkspaceBoardSectionUrl } from "$lib/urls";
    import type { CreateOrUpdateTaskModule } from "$lib/types/stores";

    export let taskModule: CreateOrUpdateTaskModule | null;
    // TODO Can we pull this out of taskModule too? Justus 2023-05-08
    export let taskOrNewTask: TaskOrNewTask;

    const canCreateOrUpdate = taskModule ? taskModule.canCreateOrUpdate : null;

    let breadCrumbTask: BreadCrumbTask;
    $: {
        if (taskOrNewTask.kind === "task") {
            const { task } = taskOrNewTask;
            if (!isBreadCrumbTask(task)) {
                throw new Error(`Failed to crumble ${task}'s bread`);
            }
            breadCrumbTask = task;
        } else {
            const { newTask } = taskOrNewTask;
            const { workspace_board_section } = newTask;
            if (!isBreadCrumbWorkspaceBoardSection(workspace_board_section)) {
                throw new Error(
                    `Failed to crumble ${workspace_board_section}'s bread`
                );
            }
            breadCrumbTask = {
                workspace_board_section,
            };
        }
    }

    const createOrUpdate = taskModule ? taskModule.createOrUpdateTask : null;
</script>

<div class="flex flex-row items-center justify-between">
    <div class="flex flex-row items-center gap-6">
        <div class="shrink-0">
            <CircleIcon
                action={{
                    kind: "a",
                    href: getDashboardWorkspaceBoardSectionUrl(
                        breadCrumbTask.workspace_board_section.uuid
                    ),
                }}
                size="medium"
                icon="close"
                disabled={false}
            />
        </div>
        <div class="text-sm font-bold text-utility">
            {breadCrumbTask.workspace_board_section.workspace_board.title} &gt;
            {breadCrumbTask.workspace_board_section.title}
            {#if breadCrumbTask.number}&gt; {breadCrumbTask.number}{/if}
        </div>
    </div>
    <div class="flex flex-row items-center gap-4">
        <SquovalIcon
            icon="dotsVertical"
            state="active"
            action={{ kind: "button", action: console.error }}
        />
        {#if createOrUpdate}
            <Button
                color="blue"
                size="small"
                disabled={!$canCreateOrUpdate}
                style={{ kind: "primary" }}
                label={$_("task-screen.save")}
                on:click={createOrUpdate}
            />
        {/if}
    </div>
</div>
