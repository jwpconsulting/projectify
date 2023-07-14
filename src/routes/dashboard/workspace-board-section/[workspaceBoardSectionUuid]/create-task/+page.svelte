<script lang="ts">
    import { readable, derived, writable } from "svelte/store";
    import Loading from "$lib/components/loading.svelte";
    import TaskCreateCard from "$lib/figma/screens/task/TaskCreateCard.svelte";
    import type { CreateTask, WorkspaceUser } from "$lib/types/workspace";
    import type { TasksPerUser, WorkspaceUserSelection } from "$lib/types/ui";
    import { createLabelSearchModule } from "$lib/stores/modules";
    import type { CreateTaskModule } from "$lib/types/stores";
    import { createTask as createTaskFn } from "$lib/repository/workspace";
    import type { PageData } from "./$types";
    import { goto } from "$lib/navigation";
    import { getDashboardWorkspaceBoardSectionUrl } from "$lib/urls";

    export let data: PageData;

    const { workspaceBoardSection } = data;

    const createTask = writable<Partial<CreateTask>>({});

    const newTask = {
        workspace_board_section: workspaceBoardSection,
    };
    const { workspace_board: workspaceBoard } = workspaceBoardSection;
    if (!workspaceBoard) {
        throw new Error("Expected workspaceBoard");
    }
    const { workspace } = workspaceBoard;
    if (!workspace) {
        throw new Error("Expected workspace");
    }

    const labelSearchModule = createLabelSearchModule(null, () =>
        console.error("Not implemented")
    );
    const createTaskModule: CreateTaskModule = {
        createOrUpdateTask: createOrUpdateTask,
        createTask,
        newTask,
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
        labelSearchModule,
    };

    async function createOrUpdateTask() {
        const { title, description } = $createTask;
        if (!title || !description) {
            throw new Error("Expected title and description");
        }
        const { newTask } = createTaskModule;
        const createTaskFull: CreateTask = {
            title,
            description,
            workspace_board_section: newTask.workspace_board_section,
            // TODO
            labels: [],
            // TODO
            deadline: null,
        };
        await createTaskFn(createTaskFull);
        await goto(
            getDashboardWorkspaceBoardSectionUrl(workspaceBoardSection.uuid)
        );
    }
</script>

{#if createTaskModule}
    <TaskCreateCard {createTaskModule} />
{:else}
    <Loading />
{/if}
