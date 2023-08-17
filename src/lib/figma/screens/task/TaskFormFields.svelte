<script lang="ts">
    // TODO rename to UpdateTaskFormFields.svelte
    import SubTaskBarComposite from "$lib/figma/screens/task/SubTaskBarComposite.svelte";
    import TaskFieldsTemplate from "$lib/figma/screens/task/TaskFieldsTemplate.svelte";
    import TaskUpdateDescription from "$lib/figma/screens/task/TaskUpdateDescription.svelte";
    import TaskUpdateDueDate from "$lib/figma/screens/task/TaskUpdateDueDate.svelte";
    import TaskUpdateLabel from "$lib/figma/screens/task/TaskUpdateLabel.svelte";
    import TaskUpdateSection from "$lib/figma/screens/task/TaskUpdateSection.svelte";
    import TaskUpdateTitle from "$lib/figma/screens/task/TaskUpdateTitle.svelte";
    import TaskUpdateUser from "$lib/figma/screens/task/TaskUpdateUser.svelte";
    import type { TaskModule } from "$lib/types/stores";
    import type {
        Label,
        SubTask,
        Task,
        WorkspaceUser,
    } from "$lib/types/workspace";

    // if this is in a store, we can get rid of this param
    export let task: Task;
    export let taskModule: TaskModule;

    let title: string = task.title;
    let description: string | undefined = task.description;
    let assignedUser: WorkspaceUser | null = task.assignee || null;
    let labels: Label[] = task.labels || [];
    let dueDate: string | null = null;
    let subTasks: SubTask[] = [];

    $: {
        // XXX what does this code here do?
        taskModule.updateTask.set({
            ...task,
            title: title,
            description: description,
            assignee: assignedUser || undefined,
            labels: labels,
            deadline: dueDate || undefined,
            sub_tasks: subTasks,
        });
    }
</script>

<TaskFieldsTemplate>
    <TaskUpdateTitle slot="title" bind:title />
    <TaskUpdateUser
        slot="assignee"
        action={taskModule.showUpdateWorkspaceUser}
        workspaceUser={assignedUser}
    />
    <TaskUpdateLabel
        slot="labels"
        action={taskModule.showUpdateLabel}
        {labels}
    />
    <TaskUpdateSection slot="section" {task} />
    <TaskUpdateDueDate slot="due-date" date={dueDate} />
    <TaskUpdateDescription slot="description" bind:description />
</TaskFieldsTemplate>
<SubTaskBarComposite {subTasks} />
