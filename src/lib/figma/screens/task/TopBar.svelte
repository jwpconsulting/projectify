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

    export let taskOrNewTask: TaskOrNewTask;

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
</script>

<div class="flex flex-row items-center justify-between">
    <div class="flex flex-row items-center gap-6">
        <div class="shrink-0">
            <CircleIcon size="medium" icon="close" disabled={false} />
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
        <Button
            color="blue"
            size="small"
            disabled={true}
            style={{ kind: "primary" }}
            label={$_("task-screen.save")}
        />
    </div>
</div>
