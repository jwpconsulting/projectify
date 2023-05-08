<script lang="ts">
    import TaskUpdates from "$lib/figma/screens/task/TaskUpdates.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import TaskC from "$lib/components/dashboard/task/Task.svelte";
    import TaskUpdateBar from "$lib/figma/buttons/TaskUpdateBar.svelte";
    import type { TaskUpdateBarState } from "$lib/figma/types";
    import { currentTask } from "$lib/stores/dashboard";

    export let state: TaskUpdateBarState = "updates";

    $: taskOrNewTask = $currentTask
        ? { kind: "task" as const, task: $currentTask }
        : null;
</script>

{#if taskOrNewTask && $currentTask}
    <TaskC>
        <TopBar slot="top-bar" {taskOrNewTask} taskModule={null} />
        <TaskUpdates slot="content" />
        <!-- TODO dry this up with the thing above -->
        <TaskUpdateBar
            slot="tab-bar-mobile"
            kind="mobile"
            {state}
            task={$currentTask}
        />
        <TaskUpdateBar
            slot="tab-bar-desktop"
            kind="mobile"
            {state}
            task={$currentTask}
        />
    </TaskC>
{/if}
