<script lang="ts">
    import { onMount } from "svelte";
    import { _, number } from "svelte-i18n";

    import { goto } from "$lib/navigation";
    import {
        getDashboardWorkspaceBoardSectionUrl,
        getDashboardWorkspaceBoardUrl,
        getTaskUrl,
    } from "$lib/urls";

    import Breadcrumbs from "./Breadcrumbs.svelte";
    import Form from "./Form.svelte";
    import SubTaskBarComposite from "./SubTaskBarComposite.svelte";

    import TaskUpdateBar from "$lib/figma/buttons/TaskUpdateBar.svelte";
    import Layout from "$lib/figma/screens/task/Layout.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import type { TaskUpdateBarState } from "$lib/figma/types";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { updateTask as performUpdateTask } from "$lib/repository/workspace";
    import { currentTask } from "$lib/stores/dashboard";
    import { createLabelAssignment } from "$lib/stores/dashboard/labelAssignment";
    import { createWorkspaceUserAssignment } from "$lib/stores/dashboard/workspaceUserAssignment";
    import type {
        SubTask,
        Task,
        TaskWithWorkspaceBoardSection,
        WorkspaceBoardSection,
    } from "$lib/types/workspace";
    import { coerceIsoDate } from "$lib/utils/date";
    import { unwrap } from "$lib/utils/type";

    // if this is in a store, we can get rid of this param
    // TODO
    // export let task: TaskWithWorkspaceBoardSection;
    export let task: Task;
    export let workspaceBoardSection: WorkspaceBoardSection;
    export let state: TaskUpdateBarState = "task";

    let title: string;
    let description: string | undefined;
    let dueDate: string | undefined;
    // XXX
    // This shouldn't be part of the form perhaps, we edit subtasks separately?
    // not decided yet
    let subTasks: SubTask[] | undefined;

    onMount(() => {
        populateForm();
    });

    function populateForm() {
        if (!$currentTask) {
            throw new Error("Expected currentTask");
        }
        title = $currentTask.title;
        description = $currentTask.description;
        dueDate =
            $currentTask.deadline && coerceIsoDate($currentTask.deadline);
        subTasks = $currentTask.sub_tasks;
    }

    async function action(continueEditing: boolean) {
        // TOOD add rest here
        const submitTask: TaskWithWorkspaceBoardSection = {
            ...task,
            workspace_board_section: workspaceBoardSection,
            deadline: dueDate,
            title,
            description,
        };
        // TODO add labels here
        const labels = await labelAssignment.evaluate();
        await performUpdateTask(submitTask, labels, $workspaceUserAssignment);
        if (!task.workspace_board_section) {
            throw new Error("Expected $updateTask.workspace_board_section");
        }
        if (continueEditing) {
            await goto(getTaskUrl(task.uuid));
            return;
        }
        await goto(
            getDashboardWorkspaceBoardSectionUrl(workspaceBoardSection.uuid)
        );
    }

    $: workspaceUserAssignment = createWorkspaceUserAssignment(task);
    $: labelAssignment = createLabelAssignment(task);

    // TODO
    $: canUpdate = true;

    // TODO put me in PageData?
    $: workspaceBoard = unwrap(
        workspaceBoardSection.workspace_board,
        "Expected workspaceBoard"
    );

    $: crumbs = [
        {
            label: workspaceBoard.title,
            href: getDashboardWorkspaceBoardUrl(workspaceBoard.uuid),
        },
        {
            label: workspaceBoardSection.title,
            href: getDashboardWorkspaceBoardSectionUrl(
                workspaceBoardSection.uuid
            ),
        },
        { label: $number(task.number), href: getTaskUrl(task.uuid) },
    ];
</script>

<Layout>
    <TopBar slot="top-bar" {workspaceBoardSection}>
        <Breadcrumbs slot="breadcrumbs" {crumbs} />
        <svelte:fragment slot="buttons">
            <Button
                action={{
                    kind: "submit",
                    form: "task-form",
                    disabled: !canUpdate,
                }}
                color="blue"
                size="small"
                style={{ kind: "primary" }}
                label={$_("task-screen.update.update")}
            />
            <Button
                action={{
                    kind: "button",
                    action: () => action(true),
                    disabled: !canUpdate,
                }}
                color="blue"
                size="small"
                style={{ kind: "primary" }}
                label={$_("task-screen.update.update-continue-editing")}
            />
        </svelte:fragment>
    </TopBar>
    <TaskUpdateBar slot="tab-bar-mobile" kind="mobile" {state} {task} />
    <svelte:fragment slot="content">
        <Form
            action={action.bind(null, false)}
            {workspaceUserAssignment}
            {labelAssignment}
            bind:title
            bind:workspaceBoardSection
            bind:dueDate
            bind:description
        />
        <SubTaskBarComposite {subTasks} />
    </svelte:fragment>
</Layout>
