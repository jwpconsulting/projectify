<script lang="ts">
    import type { Writable } from "svelte/store";
    import { readable, derived, writable } from "svelte/store";
    import { goto } from "$app/navigation";
    import TaskUpdateCard from "$lib/figma/screens/task/TaskUpdateCard.svelte";
    import type { Label, Task, WorkspaceUser } from "$lib/types/workspace";
    import type { TaskOrNewTask ,
        LabelSelection,
        TasksPerUser,
        WorkspaceUserSelection,
    } from "$lib/types/ui";
    import type { TaskModule } from "$lib/types/stores";
    import { currentTask } from "$lib/stores/dashboard";
    import { updateTask as performUpdateTask } from "$lib/repository/workspace";
    import { getDashboardWorkspaceBoardSectionUrl } from "$lib/urls";

    let taskOrNewTask: TaskOrNewTask | null = null;
    let taskModule: TaskModule | null = null;

    let taskOrNewTaskStore: Writable<TaskOrNewTask> | null = null;
    let updateTask: Writable<Task | null> = writable(null);

    async function createOrUpdateTask() {
        if (!$updateTask) {
            throw new Error("Expected $updateTask");
        }
        await performUpdateTask($updateTask);
        if (!$updateTask.workspace_board_section) {
            throw new Error("Expected $updateTask.workspace_board_section");
        }
        const url = getDashboardWorkspaceBoardSectionUrl(
            $updateTask.workspace_board_section.uuid
        );
        // TODO figure out how to refresh the same page
        await goto(url);
    }

    $: {
        // Only do this once in the beginning
        if ($currentTask && !taskOrNewTask) {
            taskOrNewTask = {
                kind: "task",
                task: $currentTask,
            };
            taskOrNewTaskStore = writable(taskOrNewTask);

            taskModule = {
                createOrUpdateTask,
                taskOrNewTask: taskOrNewTaskStore,
                createTask: null,
                updateTask,
                canCreateOrUpdate: derived<[typeof updateTask], boolean>(
                    [updateTask],
                    ([$updateTask], set) => {
                        set($updateTask !== null);
                    },
                    false
                ),
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
            };
        }
    }
</script>

{#if taskOrNewTask && taskModule}
    <TaskUpdateCard {taskOrNewTask} {taskModule} />
{/if}
