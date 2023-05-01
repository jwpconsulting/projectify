<script lang="ts">
    import type { Writable } from "svelte/store";
    import { readable, derived, writable } from "svelte/store";
    import { goto } from "$app/navigation";
    import TaskUpdateCard from "$lib/figma/screens/task/TaskUpdateCard.svelte";
    import type { Task } from "$lib/types/workspace";
    import type {
        TaskOrNewTask,
        LabelSelection,
        LabelSelectionInput,
        TasksPerUser,
        WorkspaceUserSelection,
        WorkspaceUserSelectionInput,
    } from "$lib/types/ui";
    import type {
        LabelSearchModule,
        WorkspaceUserSearchModule,
        TaskModule,
    } from "$lib/types/stores";
    import {
        createLabelSearchResults,
        currentWorkspaceLabels,
        currentTask,
        currentWorkspaceUsers,
        createWorkspaceUserSearchResults,
    } from "$lib/stores/dashboard";
    import {
        assignLabelToTask,
        updateTask as performUpdateTask,
        assignUserToTask,
    } from "$lib/repository/workspace";
    import { getDashboardWorkspaceBoardSectionUrl } from "$lib/urls";
    import { openContextMenu } from "$lib/stores/global-ui";

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
        if ($currentTask) {
            const task = $currentTask;
            taskOrNewTask = {
                kind: "task",
                task: task,
            };
            taskOrNewTaskStore = writable(taskOrNewTask);
            const workspaceUserSearch = writable("");
            const selected: WorkspaceUserSelection = task.assignee
                ? {
                      kind: "workspaceUsers",
                      workspaceUserUuids: new Set([task.assignee.uuid]),
                  }
                : {
                      kind: "unassigned",
                  };
            const workspaceUserSearchModule: WorkspaceUserSearchModule = {
                select: async (selection: WorkspaceUserSelectionInput) => {
                    if (!task) {
                        throw new Error("Expected $currentTask");
                    }
                    if (selection.kind === "unassigned") {
                        await assignUserToTask(null, task.uuid);
                    } else if (selection.kind === "allWorkspaceUsers") {
                        throw new Error("Unsupported");
                    } else {
                        await assignUserToTask(
                            selection.workspaceUser.user.email,
                            task.uuid
                        );
                    }
                },
                deselect: console.error,
                selected: writable<WorkspaceUserSelection>(selected),
                // XXX find a way to postpone this, albeit useful, showing
                // the amount of tasks per users right from the beginning
                // will be more work
                tasksPerUser: readable<TasksPerUser>({
                    unassigned: 0,
                    assigned: new Map(),
                }),
                search: workspaceUserSearch,
                searchResults: createWorkspaceUserSearchResults(
                    currentWorkspaceUsers,
                    workspaceUserSearch
                ),
            };
            const labelSelected: LabelSelection =
                task.labels && task.labels.length > 0
                    ? {
                          kind: "labels",
                          labelUuids: new Set(task.labels.map((l) => l.uuid)),
                      }
                    : { kind: "noLabel" };
            const labelSearch = writable("");
            const selectOrDeselectLabel = (
                select: boolean,
                labelSelectionInput: LabelSelectionInput
            ) => {
                const { kind } = labelSelectionInput;
                if (kind === "noLabel") {
                    console.error("No API for removing all labels");
                    throw new Error("TODO");
                } else if (kind === "allLabels") {
                    console.error("No API for assigning all labels");
                    throw new Error("TODO");
                } else {
                    const { labelUuid } = labelSelectionInput;
                    assignLabelToTask(task, labelUuid, select);
                }
            };
            const labelSearchModule: LabelSearchModule = {
                select: (labelSelectionInput: LabelSelectionInput) => {
                    selectOrDeselectLabel(true, labelSelectionInput);
                },
                deselect: (labelSelectionInput: LabelSelectionInput) => {
                    selectOrDeselectLabel(false, labelSelectionInput);
                },
                selected: writable<LabelSelection>(labelSelected),
                search: writable(""),
                searchResults: createLabelSearchResults(
                    currentWorkspaceLabels,
                    labelSearch
                ),
            };
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
                workspaceUserSearchModule,
                labelSearchModule,
                // TODO make label menu so that "all" can not be selected
                showUpdateWorkspaceUser: (anchor: HTMLElement) => {
                    openContextMenu(
                        {
                            kind: "updateMember",
                            workspaceUserSearchModule,
                        },
                        anchor
                    );
                },
                showUpdateLabel: (anchor: HTMLElement) => {
                    openContextMenu(
                        {
                            kind: "updateLabel",
                            labelSearchModule,
                        },
                        anchor
                    );
                },
            };
        }
    }
</script>

{#if taskOrNewTask && taskModule}
    <TaskUpdateCard {taskOrNewTask} {taskModule} />
{/if}
