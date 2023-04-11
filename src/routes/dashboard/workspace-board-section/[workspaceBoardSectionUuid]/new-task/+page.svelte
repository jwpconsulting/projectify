<script lang="ts">
    import Loading from "$lib/components/loading.svelte";
    import { page } from "$app/stores";
    import TaskUpdateCard from "$lib/figma/screens/task/TaskUpdateCard.svelte";
    import type { NewTask } from "$lib/types/workspace";
    import type { TaskOrNewTask } from "$lib/types/ui";

    import {
        currentWorkspaceBoardSection,
        currentWorkspaceBoardSectionUuid,
    } from "$lib/stores/dashboard";

    $: {
        $currentWorkspaceBoardSectionUuid =
            $page.params["workspaceBoardSectionUuid"];
        console.log($currentWorkspaceBoardSectionUuid);
    }

    let newTask: NewTask;
    let taskOrNewTask: TaskOrNewTask;

    $: {
        if ($currentWorkspaceBoardSection) {
            newTask = {
                workspace_board_section: $currentWorkspaceBoardSection,
            };
            taskOrNewTask = {
                kind: "newTask",
                newTask,
            };
        }
    }
</script>

{#if taskOrNewTask}
    <TaskUpdateCard {taskOrNewTask} />
{:else}
    <Loading />
{/if}
