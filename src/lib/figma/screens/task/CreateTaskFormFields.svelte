<script lang="ts">
    import TaskFieldsTemplate from "$lib/figma/screens/task/TaskFieldsTemplate.svelte";
    import TaskUpdateDescription from "$lib/figma/screens/task/TaskUpdateDescription.svelte";
    import TaskUpdateTitle from "$lib/figma/screens/task/TaskUpdateTitle.svelte";
    import type { CreateTaskModule } from "$lib/types/stores";

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
