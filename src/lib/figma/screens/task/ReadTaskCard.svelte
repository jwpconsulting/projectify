<script lang="ts">
    import { getTaskEditUrl } from "$lib/urls";

    import TaskC from "$lib/components/dashboard/task/Task.svelte";
    import TaskUpdateBar from "$lib/figma/buttons/TaskUpdateBar.svelte";
    import TaskFieldsTemplate from "$lib/figma/screens/task/TaskFieldsTemplate.svelte";
    import TaskLabel from "$lib/figma/screens/task/TaskLabel.svelte";
    import TaskTitle from "$lib/figma/screens/task/TaskTitle.svelte";
    import TaskUpdateDescription from "$lib/figma/screens/task/TaskUpdateDescription.svelte";
    import TaskUpdateDueDate from "$lib/figma/screens/task/TaskUpdateDueDate.svelte";
    import TaskUpdateSection from "$lib/figma/screens/task/TaskUpdateSection.svelte";
    import TaskUser from "$lib/figma/screens/task/TaskUser.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import type { TaskUpdateBarState } from "$lib/figma/types";
    import type { Task } from "$lib/types/workspace";
    import { unwrap } from "$lib/utils/type";

    export let task: Task;
    export let state: TaskUpdateBarState = "task";

    $: taskOrNewTask = { kind: "task" as const, task };
    $: workspaceBoardSection = unwrap(
        task.workspace_board_section,
        "Expected workspace_board_section"
    );
</script>

<TaskC>
    <TopBar
        slot="top-bar"
        {taskOrNewTask}
        taskModule={null}
        editLink={getTaskEditUrl(task.uuid)}
    />
    <TaskFieldsTemplate slot="content">
        <TaskTitle slot="title" title={task.title} readonly />
        <TaskUser slot="assignee" workspaceUser={task.assignee ?? null} />
        <TaskLabel slot="labels" labels={task.labels} />
        <TaskUpdateSection slot="section" {workspaceBoardSection} />
        <TaskUpdateDueDate slot="due-date" date={task.deadline ?? null} />
        <TaskUpdateDescription
            slot="description"
            readonly
            description={task.description}
        />
    </TaskFieldsTemplate>
    <TaskUpdateBar slot="tab-bar-mobile" kind="mobile" {state} {task} />
    <TaskUpdateBar slot="tab-bar-desktop" kind="mobile" {state} {task} />
</TaskC>
