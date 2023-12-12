<script lang="ts">
    import { _, number } from "svelte-i18n";

    import TaskUpdateBar from "$lib/figma/buttons/TaskUpdateBar.svelte";
    import Fields from "$lib/figma/screens/task/Fields.svelte";
    import Layout from "$lib/figma/screens/task/Layout.svelte";
    import TaskDescription from "$lib/figma/screens/task/TaskDescription.svelte";
    import TaskDueDate from "$lib/figma/screens/task/TaskDueDate.svelte";
    import TaskLabel from "$lib/figma/screens/task/TaskLabel.svelte";
    import TaskTitle from "$lib/figma/screens/task/TaskTitle.svelte";
    import TaskUser from "$lib/figma/screens/task/TaskUser.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import type { TaskUpdateBarState } from "$lib/figma/types";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";
    import { currentTask } from "$lib/stores/dashboard";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { TaskWithWorkspace } from "$lib/types/workspace";
    import {
        getDashboardWorkspaceBoardSectionUrl,
        getDashboardWorkspaceBoardUrl,
        getTaskEditUrl,
        getTaskUrl,
    } from "$lib/urls";
    import { coerceIsoDate } from "$lib/utils/date";

    import Breadcrumbs from "./Breadcrumbs.svelte";
    import ReadSubTasks from "./ReadSubTasks.svelte";

    import { goto } from "$app/navigation";

    export let task: TaskWithWorkspace;
    export let state: TaskUpdateBarState = "task";

    task = $currentTask ?? task;

    let contextMenuRef: HTMLElement;

    $: subTasks = task.sub_tasks;

    async function onInteract() {
        await goto(getTaskEditUrl(task.uuid));
    }

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
                color="blue"
                size="small"
                style={{ kind: "primary" }}
                label={$_("task-screen.edit")}
                action={{ kind: "a", href: getTaskEditUrl(task.uuid) }}
            />
            <div bind:this={contextMenuRef}>
                <SquovalIcon
                    icon="dotsVertical"
                    state="active"
                    action={{
                        kind: "button",
                        action: openContextMenu.bind(
                            null,
                            {
                                kind: "task",
                                task,
                                location: "task",
                                workspaceBoardSection,
                            },
                            contextMenuRef
                        ),
                    }}
                />
            </div>
        </svelte:fragment>
    </TopBar>
    <TaskUpdateBar slot="tab-bar-mobile" kind="mobile" {state} {task} />
    <svelte:fragment slot="content">
        <Fields>
            <TaskTitle slot="title" title={task.title} readonly {onInteract} />
            <TaskUser
                slot="assignee"
                workspaceUser={task.assignee}
                {onInteract}
            />
            <TaskLabel
                slot="labels"
                labels={task.labels}
                {onInteract}
                readonly
            />
            <TaskDueDate
                slot="due-date"
                dueDate={task.deadline && coerceIsoDate(task.deadline)}
                readonly
                {onInteract}
            />
            <TaskDescription
                slot="description"
                readonly
                description={task.description}
                {onInteract}
            />
        </Fields>
        <ReadSubTasks {subTasks} {onInteract} />
    </svelte:fragment>
</Layout>
