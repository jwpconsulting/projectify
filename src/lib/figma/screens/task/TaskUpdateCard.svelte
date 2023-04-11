<script lang="ts">
    import TaskUpdateBar from "$lib/figma/buttons/TaskUpdateBar.svelte";
    import TaskFormFields from "$lib/figma/screens/task/TaskFormFields.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import TaskUpdates from "$lib/figma/screens/task/TaskUpdates.svelte";
    import type { TaskOrNewTask } from "$lib/types/ui";
    import type { TaskUpdateBarState } from "$lib/figma/types";
    import type { TaskModule } from "$lib/types/stores";

    export let taskOrNewTask: TaskOrNewTask;
    export let taskModule: TaskModule;
    export let state: TaskUpdateBarState = "task";
</script>

<div class="block lg:hidden">
    <div class="flex h-full flex-col gap-8 p-4">
        <TopBar {taskOrNewTask} {taskModule} />
        <TaskUpdateBar kind="mobile" {state} />
        {#if state === "task"}
            <TaskFormFields {taskOrNewTask} {taskModule} />
        {:else}
            <TaskUpdates />
        {/if}
    </div>
</div>
<div class="hidden lg:block">
    <div class="flex h-full w-full flex-col gap-8 p-4">
        <TopBar {taskOrNewTask} {taskModule} />
        <div class="flex h-full w-full flex-row gap-4">
            <div class="flex w-1/2 flex-col gap-8">
                <TaskUpdateBar kind="desktop" state="task" />
                <TaskFormFields {taskOrNewTask} {taskModule} />
            </div>
            <div class="flex w-1/2 flex-col gap-4">
                <TaskUpdateBar kind="desktop" state="updates" />
                <TaskUpdates />
            </div>
        </div>
    </div>
</div>
