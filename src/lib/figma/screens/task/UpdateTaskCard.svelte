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
    import UpdateSubTasks from "./UpdateSubTasks.svelte";

    import TaskUpdateBar from "$lib/figma/buttons/TaskUpdateBar.svelte";
    import Layout from "$lib/figma/screens/task/Layout.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import type { TaskUpdateBarState } from "$lib/figma/types";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { updateTask as performUpdateTask } from "$lib/repository/workspace";
    import {
        currentTask,
        createSubTaskAssignment,
    } from "$lib/stores/dashboard";
    import { createLabelAssignment } from "$lib/stores/dashboard/labelAssignment";
    import { createWorkspaceUserAssignment } from "$lib/stores/dashboard/workspaceUserAssignment";
    import type {
        TaskWithWorkspace,
        TaskWithWorkspaceBoardSection,
    } from "$lib/types/workspace";
    import { coerceIsoDate } from "$lib/utils/date";

    // if this is in a store, we can get rid of this param
    export let task: TaskWithWorkspace;
    export let state: TaskUpdateBarState = "task";

    let title: string;
    let description: string | undefined;
    let dueDate: string | undefined;

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
    }

    async function action(continueEditing: boolean) {
        // TOOD add rest here
        const submitTask: TaskWithWorkspaceBoardSection = {
            ...task,
            deadline: dueDate,
            title,
            description,
        };
        // TODO add labels here
        await performUpdateTask(
            submitTask,
            $labelAssignment,
            $workspaceUserAssignment
        );
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
    $: subTaskAssignment = createSubTaskAssignment(task);

    // XXX I am sure we can have really fancy validation
    $: canUpdate = title !== "";

    // TODO put me in PageData?
    $: workspaceBoardSection = task.workspace_board_section;
    $: workspaceBoard = workspaceBoardSection.workspace_board;

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
        <UpdateSubTasks {subTaskAssignment} />
    </svelte:fragment>
</Layout>
