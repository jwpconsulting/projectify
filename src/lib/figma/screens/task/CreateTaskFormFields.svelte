<script lang="ts">
    import type { CreateTaskModule } from "$lib/types/stores";
    import TaskUpdateTitle from "$lib/figma/screens/task/TaskUpdateTitle.svelte";

    export let createTaskModule: CreateTaskModule;

    let { createTask } = createTaskModule;
</script>

<TaskUpdateTitle bind:title={$createTask.title} />
