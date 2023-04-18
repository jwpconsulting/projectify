<script lang="ts">
    import { readable, derived, writable } from "svelte/store";
    import Loading from "$lib/components/loading.svelte";
    import { page } from "$app/stores";
    import TaskUpdateCard from "$lib/figma/screens/task/TaskUpdateCard.svelte";
    import type {
        CreateTask,
        NewTask,
        Label,
        WorkspaceUser,
    } from "$lib/types/workspace";
    import type {
        TaskOrNewTask,
        LabelSelection,
        TasksPerUser,
        WorkspaceUserSelection,
    } from "$lib/types/ui";
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
                updateTask: null,
                canCreateOrUpdate: derived<[typeof createTask], boolean>(
                    [createTask],
                    ([$createTask], set) => {
                        set($createTask !== null);
                    },
                    false
                ),
                // XXX this requires special logic because we can only
                // assign users/labels after the task is already created
                // TODO make workspace user menu so that "all" can not be
                // selected
                workspaceUserSearchModule: {
                    select: console.error,
                    deselect: console.error,
                    selected: writable<WorkspaceUserSelection>(),
                    // XXX find a way to postpone this, albeit useful, showing
                    // the amount of tasks per users right from the beginning
                    // will be more work
                    tasksPerUser: readable<TasksPerUser>(),
                    search: writable(""),
                    searchResults: readable<WorkspaceUser[]>([]),
                },
                // TODO make label menu so that "all" can not be selected
                labelSearchModule: {
                    select: console.error,
                    deselect: console.error,
                    selected: writable<LabelSelection>(),
                    search: writable(""),
                    searchResults: readable<Label[]>([]),
                },
                showUpdateWorkspaceUser: () => {
                    throw new Error("Not implement");
                },
                showUpdateLabel: () => {
                    throw new Error("Not implement");
                },
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
