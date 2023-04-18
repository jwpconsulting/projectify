<script lang="ts">
    import type { Writable } from "svelte/store";
    import { derived, writable } from "svelte/store";
    import { goto } from "$app/navigation";
    import TaskUpdateCard from "$lib/figma/screens/task/TaskUpdateCard.svelte";
    import type { Task } from "$lib/types/workspace";
    import type { TaskOrNewTask } from "$lib/types/ui";
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
            };
        }
    }
</script>

{#if taskOrNewTask && taskModule}
    <TaskUpdateCard {taskOrNewTask} {taskModule} />
{/if}
