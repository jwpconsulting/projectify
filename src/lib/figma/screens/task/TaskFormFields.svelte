<script lang="ts">
    // TODO rename to UpdateTaskFormFields.svelte
    import TaskUpdateTitle from "$lib/figma/screens/task/TaskUpdateTitle.svelte";
    import TaskUpdateUser from "$lib/figma/screens/task/TaskUpdateUser.svelte";
    import TaskUpdateLabel from "$lib/figma/screens/task/TaskUpdateLabel.svelte";
    import TaskUpdateDueDate from "$lib/figma/screens/task/TaskUpdateDueDate.svelte";
    import TaskUpdateDescription from "$lib/figma/screens/task/TaskUpdateDescription.svelte";
    import SubTaskBarComposite from "$lib/figma/screens/task/SubTaskBarComposite.svelte";
    import type { TaskModule } from "$lib/types/stores";
    import type { TaskOrNewTask } from "$lib/types/ui";
    import type {
        CreateTask,
        Label,
        SubTask,
        WorkspaceUser,
    } from "$lib/types/workspace";

    // if this is in a store, we can get rid of this param
    export let taskOrNewTask: TaskOrNewTask;
    export let taskModule: TaskModule;

    let title: string | undefined = undefined;
    let description: string | undefined = undefined;
    let assignedUser: WorkspaceUser | null = null;
    let labels: Label[] = [];
    let dueDate: string | null = null;
    let subTasks: SubTask[] = [];

    let createTask: CreateTask | null;

    $: {
        if (taskOrNewTask.kind === "task") {
            const { task } = taskOrNewTask;
            title ||= task.title;
            description ||= task.description || undefined;
            if (task.assignee) {
                assignedUser ||= task.assignee;
            }
            labels = task.labels;
            dueDate ||= task.deadline || null;
            subTasks = task.sub_tasks || [];
            // Then: Subscribe to changes of fields an assign them back to
            // taskOrNewTask.task

            if (taskModule.updateTask) {
                // XXX what does this code here do?
                const { task } = taskOrNewTask;
                taskModule.updateTask.set({
                    ...task,
                    title: title || task.title,
                    description: description || undefined,
                    assignee: assignedUser || undefined,
                    labels: labels,
                    deadline: dueDate || undefined,
                    sub_tasks: subTasks,
                });
            }
        } else {
            // XXX form validation goes here
            const { newTask } = taskOrNewTask;
            if (title && description && taskModule.createTask) {
                createTask = {
                    title,
                    description,
                    labels,
                    deadline: dueDate,
                    assignee: assignedUser || undefined,
                    workspace_board_section: newTask.workspace_board_section,
                };
                taskModule.createTask.set(createTask);
            }
        }
    }
</script>

<TaskUpdateTitle bind:title />
<TaskUpdateUser
    action={taskModule.showUpdateWorkspaceUser}
    workspaceUser={assignedUser}
/>
<TaskUpdateLabel action={taskModule.showUpdateLabel} {labels} />
<!-- TODO section -->
<TaskUpdateDueDate date={dueDate} />
<!-- TODO select watcher -->
<TaskUpdateDescription bind:description />
<!-- BIND me back -->
<SubTaskBarComposite {subTasks} />
