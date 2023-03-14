<script lang="ts">
    import { _ } from "svelte-i18n";
    import SubTaskProgress from "$lib/figma/buttons/SubTaskProgress.svelte";
    import Title from "$lib/figma/cards/task-card/Title.svelte";
    import Labels from "$lib/figma/cards/task-card/Labels.svelte";
    import WorkspaceUser from "$lib/figma/cards/task-card/WorkspaceUser.svelte";
    import Chevrons from "$lib/figma/cards/task-card/Chevrons.svelte";
    import MenuButton from "$lib/figma/cards/task-card/MenuButton.svelte";
    import type { WorkspaceBoardSection, Task } from "$lib/types/workspace";
    import {
        currentWorkspaceBoardUuid,
        openTaskDetails,
    } from "$lib/stores/dashboard";

    export let task: Task;
    export let workspaceBoardSection: WorkspaceBoardSection | null = null;

    export let isFirst = false;
    export let isLast = false;

    function onClick() {
        if (!$currentWorkspaceBoardUuid) {
            throw new Error("Expected $currentWorkspaceBoardUuid");
        }
        openTaskDetails($currentWorkspaceBoardUuid, task.uuid);
    }
</script>

<button
    class="box-border w-full rounded-lg border border-base-300 bg-base-100 p-2"
    on:click={onClick}
    data-uuid={task.uuid}
>
    <div class="flex flex-col md:hidden">
        <div class="flex flex-row justify-between">
            <div class="">
                <Title {task} />
            </div>
            <div class="flex flex-row items-center gap-2 justify-self-end">
                <Chevrons {task} {isFirst} {isLast} {workspaceBoardSection} />
                <MenuButton {task} {workspaceBoardSection} />
            </div>
        </div>
        <div class="flex flex-row justify-between">
            <div class="col-span-3 flex flex-row sm:col-span-4">
                <Labels {task} />
            </div>
            <div
                class="col-span-3 flex flex-row justify-self-end sm:col-span-2"
            >
                <div class="flex flex-row items-center gap-4">
                    <SubTaskProgress {task} />
                </div>
                <div class="flex flex-row items-center">
                    <WorkspaceUser {task} />
                </div>
            </div>
        </div>
    </div>
    <div class="hidden w-full flex-row justify-between md:flex">
        <div class="flex flex-row items-center">
            <Title {task} />
        </div>
        <div class="flex flex-row items-center justify-start gap-6">
            <Labels {task} />
        </div>
        <div class="flex flex-row items-center justify-end gap-2">
            <div class="flex flex-row items-center gap-4">
                <SubTaskProgress {task} />
            </div>
            <div class="flex flex-row items-center gap-2">
                <WorkspaceUser {task} />
                <div>
                    <div class="flex flex-row items-center">
                        <Chevrons
                            {task}
                            {isFirst}
                            {isLast}
                            {workspaceBoardSection}
                        />
                        <MenuButton {task} {workspaceBoardSection} />
                    </div>
                </div>
            </div>
        </div>
    </div>
</button>
