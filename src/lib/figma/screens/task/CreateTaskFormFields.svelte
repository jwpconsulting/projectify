<script lang="ts">
    import type { CreateTaskModule } from "$lib/types/stores";
    import TaskUpdateTitle from "$lib/figma/screens/task/TaskUpdateTitle.svelte";
    import TaskUpdateDescription from "$lib/figma/screens/task/TaskUpdateDescription.svelte";

    export let createTaskModule: CreateTaskModule;

    let { createTask } = createTaskModule;
</script>

<TaskUpdateTitle bind:title={$createTask.title} />
<TaskUpdateDescription bind:description={$createTask.description} />
