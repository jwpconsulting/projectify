<script lang="ts">
    import type { CreateTaskModule } from "$lib/types/stores";
    import TaskUpdateTitle from "$lib/figma/screens/task/TaskUpdateTitle.svelte";
    import TaskUpdateDescription from "$lib/figma/screens/task/TaskUpdateDescription.svelte";
    import TaskFieldsTemplate from "$lib/figma/screens/task/TaskFieldsTemplate.svelte";

    export let createTaskModule: CreateTaskModule;

    let { createTask } = createTaskModule;
</script>

<TaskFieldsTemplate>
    <TaskUpdateTitle slot="title" bind:title={$createTask.title} />
    <TaskUpdateDescription
        slot="description"
        bind:description={$createTask.description}
    />
</TaskFieldsTemplate>
