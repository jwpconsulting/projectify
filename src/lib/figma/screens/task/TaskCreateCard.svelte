<script lang="ts">
    // TODO rename to CreateTaskCard.svelte
    import CreateTaskFormFields from "$lib/figma/screens/task/CreateTaskFormFields.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import type { CreateTaskModule } from "$lib/types/stores";

    export let createTaskModule: CreateTaskModule;

    $: taskOrNewTask = {
        kind: "newTask" as const,
        newTask: createTaskModule.newTask,
    };
</script>

<div class="block lg:hidden">
    <div class="flex h-full flex-col gap-8 p-4">
        <TopBar {taskOrNewTask} taskModule={createTaskModule} />
        <CreateTaskFormFields {createTaskModule} />
    </div>
</div>
<div class="hidden lg:block">
    <div class="flex h-full w-full flex-col gap-8 p-4">
        <TopBar {taskOrNewTask} taskModule={createTaskModule} />
        <CreateTaskFormFields {createTaskModule} />
    </div>
</div>
