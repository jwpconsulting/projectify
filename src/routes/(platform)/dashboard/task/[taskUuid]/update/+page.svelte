<script lang="ts">
    import type { Writable } from "svelte/store";
    import { readable, writable } from "svelte/store";
    import { goto } from "$lib/navigation";
    import TaskUpdateCard from "$lib/figma/screens/task/TaskUpdateCard.svelte";
    import type { Task } from "$lib/types/workspace";
    import { createLabelSearchModule } from "$lib/stores/modules";
    import {
        assignLabelToTask,
        updateTask as performUpdateTask,
        assignUserToTask,
    } from "$lib/repository/workspace";
    import type {
        TasksPerUser,
        WorkspaceUserSelection,
        WorkspaceUserSelectionInput,
    } from "$lib/types/ui";
    import type {
        WorkspaceUserSearchModule,
        TaskModule,
    } from "$lib/types/stores";
    import {
        currentWorkspaceUsers,
        createWorkspaceUserSearchResults,
    } from "$lib/stores/dashboard";
    import { getDashboardWorkspaceBoardSectionUrl } from "$lib/urls";
    import { openContextMenu } from "$lib/stores/globalUi";

    export let data: { task: Task };
    const { task } = data;
    let taskModule: TaskModule | null = null;

    let updateTask: Writable<Partial<Task>> = writable({});

    async function createOrUpdateTask() {
        if (!task) {
            throw new Error("Expected task");
        }
        // TOOD add rest here
        const submitTask: Task = {
            ...task,
            title: $updateTask.title || task.title,
            description: $updateTask.description || task.description,
        };
        await performUpdateTask(submitTask);
        if (!task.workspace_board_section) {
            throw new Error("Expected $updateTask.workspace_board_section");
        }
        const url = getDashboardWorkspaceBoardSectionUrl(
            task.workspace_board_section.uuid
        );
        // TODO figure out how to refresh the same page
        await goto(url);
    }

    $: {
        // Only do this once in the beginning
        const { workspace_board_section: workspaceBoardSection } = task;
        if (!workspaceBoardSection) {
            throw new Error("Expected workspaceBoardSection");
        }
        const { workspace_board: workspaceBoard } = workspaceBoardSection;
        if (!workspaceBoard) {
            throw new Error("Expected workspaceBoard");
        }
        const { workspace } = workspaceBoard;
        if (!workspace) {
            throw new Error("Expected workspace");
        }
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
        const labelSearchModule = createLabelSearchModule(
            task,
            (labelUuid: string, selected: boolean) => {
                if (!task) {
                    // TODO make task non nullable here
                    throw new Error("Expected task");
                }
                assignLabelToTask(task, labelUuid, selected);
            }
        );
        taskModule = {
            task,
            createOrUpdateTask,
            updateTask,
            // We might want to add some more sophisticated rules
            // as to when and when not this can be updated
            canCreateOrUpdate: readable(true),
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
</script>

{#if task && taskModule}
    <TaskUpdateCard {task} {taskModule} />
{/if}
