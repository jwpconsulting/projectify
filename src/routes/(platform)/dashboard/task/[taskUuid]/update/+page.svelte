<script lang="ts">
    import type { Writable } from "svelte/store";
    import { readable, writable } from "svelte/store";

    import { goto } from "$lib/navigation";
    import { getDashboardWorkspaceBoardSectionUrl } from "$lib/urls";

    import type { PageData } from "./$types";

    import UpdateTaskCard from "$lib/figma/screens/task/UpdateTaskCard.svelte";
    import {
        assignLabelToTask,
        updateTask as performUpdateTask,
    } from "$lib/repository/workspace";
    import { createLabelSearchStore } from "$lib/stores/dashboard/labelAssignment";
    import { createWorkspaceUserSearchStore } from "$lib/stores/dashboard/workspaceUserAssignment";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { TaskModule } from "$lib/types/stores";
    import type { Task } from "$lib/types/workspace";

    export let data: PageData;
    const { task, workspaceBoardSection } = data;

    const updateTask: Writable<Partial<Task>> = writable({});

    async function createOrUpdateTask() {
        // TOOD add rest here
        const submitTask: Task = {
            ...task,
            title: $updateTask.title ?? task.title,
            description: $updateTask.description ?? task.description,
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

    const workspaceUserFilter = createWorkspaceUserSearchStore(task);
    const labelSearchModule = createLabelSearchStore(
        task,
        async (labelUuid: string, selected: boolean) => {
            await assignLabelToTask(task, labelUuid, selected);
        }
    );
    const taskModule: TaskModule = {
        task,
        createOrUpdateTask,
        updateTask,
        // We might want to add some more sophisticated rules
        // as to when and when not this can be updated
        canCreateOrUpdate: readable(true),
        // TODO make workspace user menu so that "all" can not be
        // selected
        workspaceUserFilter,
        labelSearchModule,
        // TODO make label menu so that "all" can not be selected
        showUpdateWorkspaceUser: (anchor: HTMLElement) => {
            openContextMenu(
                {
                    kind: "updateMember",
                    workspaceUserFilter,
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
</script>

<UpdateTaskCard {workspaceBoardSection} {task} {taskModule} />
