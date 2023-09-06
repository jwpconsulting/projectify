<script lang="ts">
    import TaskC from "$lib/components/dashboard/task/Task.svelte";
    import TaskDescription from "$lib/figma/screens/task/TaskDescription.svelte";
    import TaskFieldsTemplate from "$lib/figma/screens/task/TaskFieldsTemplate.svelte";
    import TaskSection from "$lib/figma/screens/task/TaskSection.svelte";
    import TaskTitle from "$lib/figma/screens/task/TaskTitle.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import type { CreateTaskModule } from "$lib/types/stores";
    import type { WorkspaceBoardSection } from "$lib/types/workspace";

    export let createTaskModule: CreateTaskModule;
    export let workspaceBoardSection: WorkspaceBoardSection;

    const { newTask, createTask } = createTaskModule;
</script>

<TaskC>
    <TopBar
        slot="top-bar"
        breadcrumb={{ workspaceBoardSection }}
        taskModule={createTaskModule}
    />

    <TaskFieldsTemplate slot="content">
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
</TaskC>
