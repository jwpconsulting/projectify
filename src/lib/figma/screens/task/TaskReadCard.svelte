<script lang="ts">
    import TaskUpdateBar from "$lib/figma/buttons/TaskUpdateBar.svelte";
    import TaskFields from "$lib/figma/screens/task/TaskFields.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import TaskUpdates from "$lib/figma/screens/task/TaskUpdates.svelte";
    import type { Task } from "$lib/types/workspace";
    import type { TaskUpdateBarState } from "$lib/figma/types";

    export let task: Task;
    export let state: TaskUpdateBarState = "task";

    $: taskOrNewTask = { kind: "task" as const, task };
</script>

<div class="block lg:hidden">
    <div class="flex h-full flex-col gap-8 p-4">
        <TopBar {taskOrNewTask} taskModule={null} />
        <TaskUpdateBar kind="mobile" {state} />
        {#if state === "task"}
            <TaskFields {task} />
        {:else}
            <TaskUpdates />
        {/if}
    </div>
</div>
<div class="hidden lg:block">
    <div class="flex h-full w-full flex-col gap-8 p-4">
        <TopBar {taskOrNewTask} taskModule={null} />
        <div class="flex h-full w-full flex-row gap-4">
            <div class="flex w-1/2 flex-col gap-8">
                <TaskUpdateBar kind="desktop" state="task" />
                <TaskFields {task} />
            </div>
            <div class="flex w-1/2 flex-col gap-4">
                <TaskUpdateBar kind="desktop" state="updates" />
                <TaskUpdates />
            </div>
        </div>
    </div>
</div>
