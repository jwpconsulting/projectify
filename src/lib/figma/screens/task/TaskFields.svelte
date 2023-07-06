<script lang="ts">
    import { _ } from "svelte-i18n";
    import type { Task } from "$lib/types/workspace";
    import TaskUpdateTitle from "$lib/figma/screens/task/TaskUpdateTitle.svelte";
    import TaskUpdateUser from "$lib/figma/screens/task/TaskUpdateUser.svelte";
    import TaskUpdateLabel from "$lib/figma/screens/task/TaskUpdateLabel.svelte";
    import TaskUpdateSection from "$lib/figma/screens/task/TaskUpdateSection.svelte";
    import TaskUpdateDueDate from "$lib/figma/screens/task/TaskUpdateDueDate.svelte";

    export let task: Task;
    // XXX refactor the dl dt dd structure into
    // src/lib/figma/screens/task/TaskFieldsTemplate.svelte
    // and add a slot for each form field thing
</script>

<dl class="inline-grid max-w-sm auto-cols-min grid-cols-2 items-center gap-8">
    <dt class="font-bold">
        {$_("task-screen.task-title")}
    </dt>
    <dd>
        <TaskUpdateTitle title={task.title} readonly />
    </dd>
    <dt class="font-bold">
        {$_("task-screen.assignee")}
    </dt>
    <dd>
        <TaskUpdateUser workspaceUser={task.assignee || null} />
    </dd>
    <dt class="font-bold">
        {$_("task-screen.labels")}
    </dt>
    <dd>
        <TaskUpdateLabel labels={task.labels} />
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
        <TaskUpdateDueDate date={task.deadline || null} />
    </dd>
</dl>
