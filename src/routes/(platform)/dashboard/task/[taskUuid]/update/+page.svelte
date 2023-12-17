<script lang="ts">
    import { _, number } from "svelte-i18n";

    import TaskUpdateBar from "$lib/figma/buttons/TaskUpdateBar.svelte";
    import Breadcrumbs from "$lib/figma/screens/task/Breadcrumbs.svelte";
    import Form from "$lib/figma/screens/task/Form.svelte";
    import Layout from "$lib/figma/screens/task/Layout.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import UpdateSubTasks from "$lib/figma/screens/task/UpdateSubTasks.svelte";
    import type { TaskUpdateBarState } from "$lib/figma/types";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { goto } from "$lib/navigation";
    import { updateTask as performUpdateTask } from "$lib/repository/workspace";
    import { createSubTaskAssignment } from "$lib/stores/dashboard";
    import { createLabelAssignment } from "$lib/stores/dashboard/labelAssignment";
    import { createWorkspaceUserAssignment } from "$lib/stores/dashboard/workspaceUserAssignment";
    import type { TaskWithWorkspaceBoardSection } from "$lib/types/workspace";
    import {
        getDashboardWorkspaceBoardSectionUrl,
        getDashboardWorkspaceBoardUrl,
        getTaskUrl,
    } from "$lib/urls";
    import { coerceIsoDate } from "$lib/utils/date";

    import type { PageData } from "./$types";

    export let data: PageData;
    const { task } = data;
    const { workspace_board_section: workspaceBoardSection } = task;
    const { workspace_board: workspaceBoard } = workspaceBoardSection;

    const state: TaskUpdateBarState = "task";

    // Initial data
    let { title, description } = task;
    let dueDate = task.deadline && coerceIsoDate(task.deadline);

    $: workspaceUserAssignment = createWorkspaceUserAssignment(task);
    $: labelAssignment = createLabelAssignment(task);
    $: subTaskAssignment = createSubTaskAssignment(task);
    $: subTasks = subTaskAssignment.subTasks;

    // XXX I am sure we can have really fancy validation
    $: canUpdate = title !== "" && $subTasks !== undefined;

    async function action(continueEditing: boolean) {
        if (!$labelAssignment) {
            throw new Error("Expected $labelAssignment");
        }
        const submitTask: TaskWithWorkspaceBoardSection = {
            ...task,
            deadline: dueDate,
            title,
            description,
        };
        await performUpdateTask(
            submitTask,
            $labelAssignment,
            $workspaceUserAssignment,
            $subTasks,
            { fetch }
        );
        if (continueEditing) {
            await goto(getTaskUrl(task.uuid));
            return;
        }
        await goto(
            getDashboardWorkspaceBoardSectionUrl(workspaceBoardSection.uuid)
        );
    }

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
        // We could add a better task name here, or even
        // extract the whole thing as a layout for any task/[taskUuid] route
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
            bind:dueDate
            bind:description
        />
        <UpdateSubTasks {subTaskAssignment} />
    </svelte:fragment>
</Layout>
