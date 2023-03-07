<script lang="ts">
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import TaskUpdateBar from "$lib/figma/buttons/TaskUpdateBar.svelte";
    import TaskFormFields from "$lib/figma/screens/task/TaskFormFields.svelte";
    import TaskUpdates from "$lib/figma/screens/task/TaskUpdates.svelte";

    import type { Task } from "$lib/types/workspace";

    export let task: Task;
</script>

<div class="flex h-full w-full flex-col gap-8 p-4">
    <TopBar />
    <div class="flex h-full w-full flex-row gap-4">
        <div class="flex w-1/2 flex-col gap-8">
            <TaskUpdateBar kind="desktop" state="task" />
            <TaskFormFields {task} />
        </div>
        <div class="flex w-1/2 flex-col gap-4">
            <TaskUpdateBar kind="desktop" state="updates" />
            <TaskUpdates />
        </div>
    </div>
</div>
