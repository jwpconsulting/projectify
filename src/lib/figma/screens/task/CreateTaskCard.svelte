<script lang="ts">
    // TODO rename to CreateTaskCard.svelte
    import TaskC from "$lib/components/dashboard/task/Task.svelte";
    import CreateTaskFormFields from "$lib/figma/screens/task/CreateTaskFormFields.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import type { CreateTaskModule } from "$lib/types/stores";

    export let createTaskModule: CreateTaskModule;

    $: taskOrNewTask = {
        kind: "newTask" as const,
        newTask: createTaskModule.newTask,
    };
</script>

<TaskC>
    <TopBar slot="top-bar" {taskOrNewTask} taskModule={createTaskModule} />
    <CreateTaskFormFields slot="content" {createTaskModule} />
</TaskC>
