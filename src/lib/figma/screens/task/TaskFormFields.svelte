<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Minus } from "@steeze-ui/heroicons";

    import TaskUpdateUser from "$lib/figma/screens/task/TaskUpdateUser.svelte";
    import TaskUpdateLabel from "$lib/figma/screens/task/TaskUpdateLabel.svelte";
    import TaskUpdateDueDate from "$lib/figma/screens/task/TaskUpdateDueDate.svelte";
    import SubTaskBar from "$lib/figma/screens/task/SubTaskBar.svelte";
    import type { TaskOrNewTask } from "$lib/types/ui";
    import type { User } from "$lib/types/user";
    import type { Label } from "$lib/types/workspace";

    export let taskOrNewTask: TaskOrNewTask;

    let assignedUser: User | null = null;
    let labels: Label[] = [];
    let dueDate: string | null = null;
    $: {
        if (taskOrNewTask.kind === "task") {
            const task = taskOrNewTask.task;
            if (task.assignee) {
                assignedUser = task.assignee.user;
            }
            labels = task.labels;
            dueDate = task.deadline || null;
        }
    }
</script>

<div class="flex flex-row gap-2">
    <Icon src={Minus} class="w-6" theme="outline" />
    NEW TASK NAME
</div>
<TaskUpdateUser user={assignedUser} />
<TaskUpdateLabel {labels} />
<!-- TODO section -->
<TaskUpdateDueDate date={dueDate} />
<!-- TODO select watcher -->
<!-- TODO description -->
<SubTaskBar progress={0} />
