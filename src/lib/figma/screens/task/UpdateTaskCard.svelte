<script lang="ts">
    import type { Writable } from "svelte/store";
    import { readable, writable } from "svelte/store";
    import { _, number } from "svelte-i18n";

    import { goto } from "$lib/navigation";
    import {
        getDashboardWorkspaceBoardSectionUrl,
        getDashboardWorkspaceBoardUrl,
        getTaskUrl,
    } from "$lib/urls";

    import Breadcrumbs from "./Breadcrumbs.svelte";

    import TaskC from "$lib/components/dashboard/task/Task.svelte";
    import TaskUpdateBar from "$lib/figma/buttons/TaskUpdateBar.svelte";
    import SubTaskBarComposite from "$lib/figma/screens/task/SubTaskBarComposite.svelte";
    import TaskDescription from "$lib/figma/screens/task/TaskDescription.svelte";
    import TaskDueDate from "$lib/figma/screens/task/TaskDueDate.svelte";
    import TaskFieldsTemplate from "$lib/figma/screens/task/TaskFieldsTemplate.svelte";
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
    import type { TaskModule } from "$lib/types/stores";
    import type {
        Label,
        SubTask,
        Task,
        WorkspaceBoardSection,
        WorkspaceUser,
    } from "$lib/types/workspace";
    import { unwrap } from "$lib/utils/type";

    // if this is in a store, we can get rid of this param
    export let task: Task;
    export let workspaceBoardSection: WorkspaceBoardSection;
    export let state: TaskUpdateBarState = "task";

    let title: string = task.title;
    let description: string | undefined = task.description;
    const assignedUser: WorkspaceUser | null = task.assignee ?? null;
    const labels: Label[] = task.labels;
    const dueDate: string | undefined = undefined;
    const subTasks: SubTask[] = [];

    const updateTask: Writable<Partial<Task>> = writable({});

    async function createOrUpdateTask() {
        // TOOD add rest here
        const submitTask: Task = {
            ...task,
            title: $updateTask.title ?? task.title,
            description: $updateTask.description ?? task.description,
        };
        // TODO add labels here
        const labels = await taskModule.labelAssignment.evaluate();
        await performUpdateTask(submitTask, labels);
        if (!task.workspace_board_section) {
            throw new Error("Expected $updateTask.workspace_board_section");
        }
        const url = getDashboardWorkspaceBoardSectionUrl(
            task.workspace_board_section.uuid
        );
        // TODO figure out how to refresh the same page
        await goto(url);
    }

    const workspaceUserAssignment = createWorkspaceUserAssignment(task);
    const labelAssignment = createLabelAssignment(task);
    // TODO
    const canCreateOrUpdate = readable(true);
    const taskModule: TaskModule = {
        task,
        updateTask,
        // TODO make workspace user menu so that "all" can not be
        // selected
        workspaceUserAssignment,
        labelAssignment,
        // TODO make label menu so that "all" can not be selected
        showUpdateWorkspaceUser: (anchor: HTMLElement) => {
            openContextMenu(
                {
                    kind: "updateMember",
                    workspaceUserAssignment,
                },
                anchor
            );
        },
        showUpdateLabel: (anchor: HTMLElement) => {
            openContextMenu(
                {
                    kind: "updateLabel",
                    labelAssignment,
                },
                anchor
            );
        },
    };

    $: {
        // XXX what does this code here do?
        taskModule.updateTask.set({
            ...task,
            title: title,
            description: description,
            // XXX What would RMS do??
            assignee: assignedUser ?? undefined,
            labels: labels,
            deadline: dueDate ?? undefined,
            sub_tasks: subTasks,
        });
    }

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

<TaskC>
    <TopBar slot="top-bar" {workspaceBoardSection}>
        <Breadcrumbs slot="breadcrumbs" {crumbs} />
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
    <TaskUpdateBar slot="tab-bar-mobile" kind="mobile" {state} {task} />
    <TaskUpdateBar slot="tab-bar-desktop" kind="mobile" {state} {task} />
    <TaskFieldsTemplate slot="content">
        <TaskTitle slot="title" bind:title />
        <TaskUser
            slot="assignee"
            action={taskModule.showUpdateWorkspaceUser}
            workspaceUser={assignedUser}
        />
        <TaskLabel
            slot="labels"
            action={taskModule.showUpdateLabel}
            {labels}
        />
        <TaskSection slot="section" {workspaceBoardSection} />
        <TaskDueDate slot="due-date" date={dueDate} />
        <TaskDescription slot="description" bind:description />
    </TaskFieldsTemplate>
    <SubTaskBarComposite {subTasks} />
</TaskC>
