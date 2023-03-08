<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Minus } from "@steeze-ui/heroicons";

    import TaskUpdateUser from "$lib/figma/screens/task/TaskUpdateUser.svelte";
    import TaskUpdateLabel from "$lib/figma/screens/task/TaskUpdateLabel.svelte";
    import TaskUpdateDueDate from "$lib/figma/screens/task/TaskUpdateDueDate.svelte";
    import SubTaskBar from "$lib/figma/screens/task/SubTaskBar.svelte";
    import type { Task } from "$lib/types/workspace";
    import type { User } from "$lib/types/user";

    export let task: Task;

    let assignedUser: User | null = null;
    $: {
        if (task.assignee) {
            assignedUser = task.assignee.user;
        }
    }
</script>

<div class="flex flex-row gap-2">
    <Icon src={Minus} class="w-6" theme="outline" />
    NEW TASK NAME
</div>
<TaskUpdateUser user={assignedUser} />
<TaskUpdateLabel labels={task.labels} />
<!-- TODO section -->
<TaskUpdateDueDate date={task.deadline || null} />
<!-- TODO select watcher -->
<!-- TODO description -->
<SubTaskBar progress={0} />
