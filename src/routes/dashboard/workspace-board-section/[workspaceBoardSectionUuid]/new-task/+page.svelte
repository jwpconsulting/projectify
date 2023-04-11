<script lang="ts">
    import { derived, writable } from "svelte/store";
    import Loading from "$lib/components/loading.svelte";
    import { page } from "$app/stores";
    import TaskUpdateCard from "$lib/figma/screens/task/TaskUpdateCard.svelte";
    import type { CreateTask, NewTask } from "$lib/types/workspace";
    import type { TaskOrNewTask } from "$lib/types/ui";
    import type { TaskModule } from "$lib/types/stores";

    import {
        currentWorkspaceBoardSection,
        currentWorkspaceBoardSectionUuid,
    } from "$lib/stores/dashboard";
    import { createTask as createTaskFn } from "$lib/repository/workspace";

    $: {
        $currentWorkspaceBoardSectionUuid =
            $page.params["workspaceBoardSectionUuid"];
        console.log($currentWorkspaceBoardSectionUuid);
    }

    let taskModule: TaskModule;
    let newTask: NewTask;
    let taskOrNewTask: TaskOrNewTask;
    const createTask = writable<CreateTask | null>(null);

    $: {
        if ($currentWorkspaceBoardSection) {
            newTask = {
                workspace_board_section: $currentWorkspaceBoardSection,
            };
            taskOrNewTask = {
                kind: "newTask",
                newTask,
            };
            taskModule = {
                createOrUpdateTask: createOrUpdateTask,
                taskOrNewTask: writable(taskOrNewTask),
                createTask,
                canCreateOrUpdate: derived<[typeof createTask], boolean>(
                    [createTask],
                    ([$createTask], set) => {
                        set($createTask !== null);
                    },
                    false
                ),
            };
        }
    }

    function createOrUpdateTask() {
        if (!$createTask) {
            throw new Error("Expected $createTask");
        }
        createTaskFn($createTask);
    }
</script>

{#if taskOrNewTask}
    <TaskUpdateCard {taskOrNewTask} {taskModule} />
{:else}
    <Loading />
{/if}
