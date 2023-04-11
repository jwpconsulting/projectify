<script lang="ts">
    import TaskUpdateBar from "$lib/figma/buttons/TaskUpdateBar.svelte";
    import TaskFormFields from "$lib/figma/screens/task/TaskFormFields.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import TaskUpdates from "$lib/figma/screens/task/TaskUpdates.svelte";

    import type { TaskUpdateBarState } from "$lib/figma/types";
    import type { TaskOrNewTask } from "$lib/types/ui";

    export let taskOrNewTask: TaskOrNewTask;
    export let state: TaskUpdateBarState = "task";
</script>

<div class="flex h-full flex-col gap-8 p-4">
    <TopBar />
    <TaskUpdateBar kind="mobile" {state} />
    {#if state === "task"}
        <TaskFormFields {taskOrNewTask} />
    {:else}
        <TaskUpdates />
    {/if}
</div>
