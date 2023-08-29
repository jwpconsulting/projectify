<script lang="ts">
    import TaskFieldsTemplate from "$lib/figma/screens/task/TaskFieldsTemplate.svelte";
    import TaskUpdateDescription from "$lib/figma/screens/task/TaskUpdateDescription.svelte";
    import TaskUpdateSection from "$lib/figma/screens/task/TaskUpdateSection.svelte";
    import TaskUpdateTitle from "$lib/figma/screens/task/TaskUpdateTitle.svelte";
    import type { CreateTaskModule } from "$lib/types/stores";

    export let createTaskModule: CreateTaskModule;

    let { newTask, createTask } = createTaskModule;
</script>

<TaskFieldsTemplate>
    <TaskUpdateTitle slot="title" bind:title={$createTask.title} />
    <TaskUpdateSection
        slot="section"
        workspaceBoardSection={newTask.workspace_board_section}
    />
    <TaskUpdateDescription
        slot="description"
        bind:description={$createTask.description}
    />
</TaskFieldsTemplate>
