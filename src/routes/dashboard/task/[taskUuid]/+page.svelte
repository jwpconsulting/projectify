<script lang="ts">
    import { writable } from "svelte/store";
    import TaskUpdateCard from "$lib/figma/screens/task/TaskUpdateCard.svelte";
    import type { TaskOrNewTask } from "$lib/types/ui";
    import type { TaskModule } from "$lib/types/stores";
    import { currentTask } from "$lib/stores/dashboard";

    function createOrUpdateTask() {
        console.error("TODO");
    }

    let taskOrNewTask: TaskOrNewTask | null = null;
    let taskModule: TaskModule | null = null;

    $: {
        // Only do this once in the beginning
        if ($currentTask && !taskOrNewTask) {
            taskOrNewTask = {
                kind: "task",
                task: $currentTask,
            };
            taskModule = {
                createOrUpdateTask,
                taskOrNewTask: writable(taskOrNewTask),
                createTask: writable(null),
                canCreateOrUpdate: writable(false),
            };
        }
    }
</script>

{#if taskOrNewTask && taskModule}
    <TaskUpdateCard {taskOrNewTask} {taskModule} />
{/if}
