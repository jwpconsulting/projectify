<script lang="ts">
    import { _ } from "svelte-i18n";
    // TODO rename to UpdateTaskFormFields.svelte
    import TaskUpdateTitle from "$lib/figma/screens/task/TaskUpdateTitle.svelte";
    import TaskUpdateUser from "$lib/figma/screens/task/TaskUpdateUser.svelte";
    import TaskUpdateLabel from "$lib/figma/screens/task/TaskUpdateLabel.svelte";
    import TaskUpdateDueDate from "$lib/figma/screens/task/TaskUpdateDueDate.svelte";
    import TaskUpdateDescription from "$lib/figma/screens/task/TaskUpdateDescription.svelte";
    import TaskUpdateSection from "$lib/figma/screens/task/TaskUpdateSection.svelte";
    import SubTaskBarComposite from "$lib/figma/screens/task/SubTaskBarComposite.svelte";
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

<dl class="inline-grid max-w-sm auto-cols-min grid-cols-2 items-center gap-8">
    <dt class="font-bold">
        {$_("task-screen.task-title")}
    </dt>
    <dd>
        <TaskUpdateTitle bind:title />
    </dd>
    <dt class="font-bold">
        {$_("task-screen.assignee")}
    </dt>
    <dd>
        <TaskUpdateUser
            action={taskModule.showUpdateWorkspaceUser}
            workspaceUser={assignedUser}
        />
    </dd>
    <dt class="font-bold">
        {$_("task-screen.labels")}
    </dt>
    <dd>
        <TaskUpdateLabel action={taskModule.showUpdateLabel} {labels} />
    </dd>
    <dt class="font-bold">
        {$_("task-screen.section")}
    </dt>
    <dd>
        <TaskUpdateSection {task} />
    </dd>
    <dt class="font-bold">
        {$_("task-screen.due-date")}
    </dt>
    <dd>
        <TaskUpdateDueDate date={dueDate} />
    </dd>
    <dt class="font-bold">
        {$_("task-screen.description")}
    </dt>
    <dd>
        <TaskUpdateDescription bind:description />
    </dd>
</dl>
<SubTaskBarComposite {subTasks} />
