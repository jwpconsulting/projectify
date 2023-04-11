<script lang="ts">
    import { _ } from "svelte-i18n";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { MenuAlt1, Minus } from "@steeze-ui/heroicons";

    import TaskUpdateUser from "$lib/figma/screens/task/TaskUpdateUser.svelte";
    import TaskUpdateLabel from "$lib/figma/screens/task/TaskUpdateLabel.svelte";
    import TaskUpdateDueDate from "$lib/figma/screens/task/TaskUpdateDueDate.svelte";
    import SubTaskBar from "$lib/figma/screens/task/SubTaskBar.svelte";
    import InputField from "$lib/figma/input-fields/InputField.svelte";
    import type { TaskModule } from "$lib/types/stores";
    import type { TaskOrNewTask } from "$lib/types/ui";
    import type {
        CreateTask,
        Label,
        WorkspaceUser,
    } from "$lib/types/workspace";

    export let taskOrNewTask: TaskOrNewTask;
    export let taskModule: TaskModule;

    let title: string | null = null;
    let description: string | null = null;
    let assignedUser: WorkspaceUser | null = null;
    let labels: Label[] = [];
    let dueDate: string | null = null;

    let createTask: CreateTask | null;

    $: {
        if (taskOrNewTask.kind === "task") {
            const task = taskOrNewTask.task;
            if (task.assignee) {
                assignedUser = task.assignee;
            }
            labels = task.labels;
            dueDate = task.deadline || null;
            title = task.title;
        } else {
            // XXX form validation goes here
            if (title && description) {
                createTask = {
                    title,
                    description,
                    labels,
                    deadline: dueDate,
                    assignee: assignedUser || undefined,
                    workspace_board_section:
                        taskOrNewTask.newTask.workspace_board_section,
                };
                taskModule.createTask.set(createTask);
            }
        }
    }
</script>

<div class="flex flex-row gap-2">
    <Icon src={Minus} class="w-6" theme="outline" />
    <InputField
        name="title"
        style={{ kind: "field", inputType: "text" }}
        bind:value={title}
        placeholder={$_("task-screen.new-task-name")}
    />
</div>
<TaskUpdateUser workspaceUser={assignedUser} />
<TaskUpdateLabel {labels} />
<!-- TODO section -->
<TaskUpdateDueDate date={dueDate} />
<!-- TODO select watcher -->
<div class="flex flex-row gap-2">
    <Icon src={MenuAlt1} class="w-6" theme="outline" />
    <InputField
        name="description"
        style={{ kind: "field", inputType: "text" }}
        bind:value={description}
        placeholder={$_("task-screen.description")}
    />
</div>
<SubTaskBar progress={0} />
