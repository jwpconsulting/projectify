<script lang="ts">
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
    import type { TaskModule } from "$lib/types/stores";
    import type {
        Label,
        SubTask,
        Task,
        WorkspaceBoardSection,
        WorkspaceUser,
    } from "$lib/types/workspace";

    // if this is in a store, we can get rid of this param
    export let task: Task;
    export let workspaceBoardSection: WorkspaceBoardSection;
    export let taskModule: TaskModule;
    export let state: TaskUpdateBarState = "task";

    let title: string = task.title;
    let description: string | undefined = task.description;
    let assignedUser: WorkspaceUser | null = task.assignee ?? null;
    let labels: Label[] = task.labels;
    let dueDate: string | null = null;
    let subTasks: SubTask[] = [];

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
</script>

<TaskC>
    <TopBar
        slot="top-bar"
        breadcrumb={{ task: task, workspaceBoardSection }}
        {taskModule}
    />
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
