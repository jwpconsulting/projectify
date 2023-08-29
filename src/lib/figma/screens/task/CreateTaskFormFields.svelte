<script lang="ts">
    import TaskDescription from "$lib/figma/screens/task/TaskDescription.svelte";
    import TaskFieldsTemplate from "$lib/figma/screens/task/TaskFieldsTemplate.svelte";
    import TaskSection from "$lib/figma/screens/task/TaskSection.svelte";
    import TaskTitle from "$lib/figma/screens/task/TaskTitle.svelte";
    import type { CreateTaskModule } from "$lib/types/stores";

    export let createTaskModule: CreateTaskModule;

    let { newTask, createTask } = createTaskModule;
</script>

<TaskFieldsTemplate>
    <TaskTitle slot="title" bind:title={$createTask.title} />
    <TaskSection
        slot="section"
        workspaceBoardSection={newTask.workspace_board_section}
    />
    <TaskDescription
        slot="description"
        bind:description={$createTask.description}
    />
</TaskFieldsTemplate>
