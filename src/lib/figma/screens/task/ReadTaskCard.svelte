<script lang="ts">
    import { getTaskEditUrl } from "$lib/urls";

    import TaskC from "$lib/components/dashboard/task/Task.svelte";
    import TaskUpdateBar from "$lib/figma/buttons/TaskUpdateBar.svelte";
    import TaskFieldsTemplate from "$lib/figma/screens/task/TaskFieldsTemplate.svelte";
    import TaskUpdateDescription from "$lib/figma/screens/task/TaskUpdateDescription.svelte";
    import TaskUpdateDueDate from "$lib/figma/screens/task/TaskUpdateDueDate.svelte";
    import TaskUpdateLabel from "$lib/figma/screens/task/TaskUpdateLabel.svelte";
    import TaskUpdateSection from "$lib/figma/screens/task/TaskUpdateSection.svelte";
    import TaskUpdateTitle from "$lib/figma/screens/task/TaskUpdateTitle.svelte";
    import TaskUpdateUser from "$lib/figma/screens/task/TaskUpdateUser.svelte";
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
        <TaskUpdateTitle slot="title" title={task.title} readonly />
        <TaskUpdateUser
            slot="assignee"
            workspaceUser={task.assignee ?? null}
        />
        <TaskUpdateLabel slot="labels" labels={task.labels} />
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
