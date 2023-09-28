<script lang="ts">
    import { _, number } from "svelte-i18n";

    import { goto } from "$lib/navigation";
    import {
        getDashboardWorkspaceBoardSectionUrl,
        getDashboardWorkspaceBoardUrl,
        getTaskUrl,
    } from "$lib/urls";

    import Breadcrumbs from "./Breadcrumbs.svelte";

    import TaskUpdateBar from "$lib/figma/buttons/TaskUpdateBar.svelte";
    import Fields from "$lib/figma/screens/task/Fields.svelte";
    import Layout from "$lib/figma/screens/task/Layout.svelte";
    import SubTaskBarComposite from "$lib/figma/screens/task/SubTaskBarComposite.svelte";
    import TaskDescription from "$lib/figma/screens/task/TaskDescription.svelte";
    import TaskDueDate from "$lib/figma/screens/task/TaskDueDate.svelte";
    import TaskLabel from "$lib/figma/screens/task/TaskLabel.svelte";
    import TaskSection from "$lib/figma/screens/task/TaskSection.svelte";
    import TaskTitle from "$lib/figma/screens/task/TaskTitle.svelte";
    import TaskUser from "$lib/figma/screens/task/TaskUser.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import type { TaskUpdateBarState } from "$lib/figma/types";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { updateTask as performUpdateTask } from "$lib/repository/workspace";
    import { createLabelAssignment } from "$lib/stores/dashboard/labelAssignment";
    import { createWorkspaceUserAssignment } from "$lib/stores/dashboard/workspaceUserAssignment";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type {
        Label,
        SubTask,
        Task,
        WorkspaceBoardSection,
        WorkspaceUser,
    } from "$lib/types/workspace";
    import { coerceIsoDate } from "$lib/utils/date";
    import { unwrap } from "$lib/utils/type";

    // if this is in a store, we can get rid of this param
    export let task: Task;
    export let workspaceBoardSection: WorkspaceBoardSection;
    export let state: TaskUpdateBarState = "task";

    let title: string = task.title;
    let description: string | undefined = task.description;
    let assignedUser: WorkspaceUser | undefined = task.assignee;
    let labels: Label[] = task.labels;
    let dueDate: string | undefined =
        task.deadline && coerceIsoDate(task.deadline);
    const subTasks: SubTask[] = [];

    async function updateTask() {
        // TOOD add rest here
        const submitTask: Task = {
            ...task,
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
        const url = getDashboardWorkspaceBoardSectionUrl(
            task.workspace_board_section.uuid
        );
        // TODO figure out how to refresh the same page
        await goto(url);
    }
    async function showUpdateWorkspaceUser(anchor: HTMLElement) {
        await openContextMenu(
            {
                kind: "updateMember",
                workspaceUserAssignment,
            },
            anchor
        );
    }
    async function showUpdateLabel(anchor: HTMLElement) {
        await openContextMenu(
            {
                kind: "updateLabel",
                labelAssignment,
            },
            anchor
        );
    }

    const workspaceUserAssignment = createWorkspaceUserAssignment(task);
    const labelAssignment = createLabelAssignment(task);

    $: assignedUser = $workspaceUserAssignment;

    $: {
        labels = $labelAssignment;
    }

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
        <Button
            slot="buttons"
            action={{
                kind: "button",
                action: updateTask,
                disabled: !canUpdate,
            }}
            color="blue"
            size="small"
            style={{ kind: "primary" }}
            label={$_("task-screen.save")}
        />
    </TopBar>
    <TaskUpdateBar slot="tab-bar-mobile" kind="mobile" {state} {task} />
    <form on:submit|preventDefault={updateTask} slot="content">
        <input type="submit" class="hidden" />
        <Fields>
            <TaskTitle slot="title" bind:title />
            <TaskUser
                slot="assignee"
                action={showUpdateWorkspaceUser}
                workspaceUser={assignedUser}
            />
            <TaskLabel slot="labels" action={showUpdateLabel} {labels} />
            <TaskSection slot="section" {workspaceBoardSection} />
            <TaskDueDate slot="due-date" bind:date={dueDate} />
            <TaskDescription slot="description" bind:description />
        </Fields>
        <SubTaskBarComposite {subTasks} />
    </form>
</Layout>
