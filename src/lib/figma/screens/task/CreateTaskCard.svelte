<script lang="ts">
    import { derived, writable } from "svelte/store";
    import { _ } from "svelte-i18n";

    import { goto } from "$lib/navigation";
    import { getDashboardWorkspaceBoardSectionUrl } from "$lib/urls";

    import TaskC from "$lib/components/dashboard/task/Task.svelte";
    import TaskDescription from "$lib/figma/screens/task/TaskDescription.svelte";
    import TaskFieldsTemplate from "$lib/figma/screens/task/TaskFieldsTemplate.svelte";
    import TaskSection from "$lib/figma/screens/task/TaskSection.svelte";
    import TaskTitle from "$lib/figma/screens/task/TaskTitle.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { createTask as createTaskFn } from "$lib/repository/workspace";
    import { createLabelAssignment } from "$lib/stores/dashboard/labelAssignment";
    import type { CreateTaskModule } from "$lib/types/stores";
    import type { WorkspaceUserSelection } from "$lib/types/ui";
    import type {
        CreateTask,
        WorkspaceBoardSection,
    } from "$lib/types/workspace";

    export let workspaceBoardSection: WorkspaceBoardSection;

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

    const labelAssignment = createLabelAssignment();
    const canCreateOrUpdate = derived<typeof createTask, boolean>(
        createTask,
        ($createTask, set) => {
            set(
                $createTask.title !== undefined &&
                    $createTask.description !== undefined
            );
        },
        false
    );
    const createTaskModule: CreateTaskModule = {
        createTask,
        newTask,
        // XXX this requires special logic because we can only
        // assign users/labels after the task is already created
        // TODO make workspace user menu so that "all" can not be
        // selected
        workspaceUserAssignment: {
            select: console.error,
            deselect: console.error,
            selected: writable<WorkspaceUserSelection>(),
        },
        // TODO make label menu so that "all" can not be selected
        labelAssignment,
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

<TaskC>
    <TopBar slot="top-bar" breadcrumb={{ workspaceBoardSection }}>
        <Button
            slot="buttons"
            action={{
                kind: "button",
                action: createOrUpdateTask,
                disabled: !$canCreateOrUpdate,
            }}
            color="blue"
            size="small"
            style={{ kind: "primary" }}
            label={$_("task-screen.save")}
        />
    </TopBar>

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
