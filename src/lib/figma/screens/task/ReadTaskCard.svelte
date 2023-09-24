<script lang="ts">
    import { _ } from "svelte-i18n";

    import { getTaskEditUrl } from "$lib/urls";

    import TaskC from "$lib/components/dashboard/task/Task.svelte";
    import TaskUpdateBar from "$lib/figma/buttons/TaskUpdateBar.svelte";
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
    import type { Task, WorkspaceBoardSection } from "$lib/types/workspace";

    export let task: Task;
    export let workspaceBoardSection: WorkspaceBoardSection;
    export let state: TaskUpdateBarState = "task";
</script>

<TaskC>
    <TopBar slot="top-bar" breadcrumb={{ task, workspaceBoardSection }}>
        <Button
            color="blue"
            size="small"
            style={{ kind: "primary" }}
            label={$_("task-screen.edit")}
            action={{ kind: "a", href: getTaskEditUrl(task.uuid) }}
        />
    </TopBar>
    <TaskFieldsTemplate slot="content">
        <TaskTitle slot="title" title={task.title} readonly />
        <TaskUser slot="assignee" workspaceUser={task.assignee ?? null} />
        <TaskLabel slot="labels" labels={task.labels} />
        <TaskSection slot="section" {workspaceBoardSection} />
        <TaskDueDate slot="due-date" date={task.deadline ?? undefined} />
        <TaskDescription
            slot="description"
            readonly
            description={task.description}
        />
    </TaskFieldsTemplate>
    <TaskUpdateBar slot="tab-bar-mobile" kind="mobile" {state} {task} />
    <TaskUpdateBar slot="tab-bar-desktop" kind="mobile" {state} {task} />
</TaskC>
