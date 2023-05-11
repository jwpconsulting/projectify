<script lang="ts">
    import { _ } from "svelte-i18n";
    import type { Task } from "$lib/types/workspace";
    import TaskUpdateTitle from "$lib/figma/screens/task/TaskUpdateTitle.svelte";
    import TaskUpdateUser from "$lib/figma/screens/task/TaskUpdateUser.svelte";
    import TaskUpdateLabel from "$lib/figma/screens/task/TaskUpdateLabel.svelte";
    import TaskUpdateSection from "$lib/figma/screens/task/TaskUpdateSection.svelte";

    export let task: Task;
</script>

<dl class="flex flex-col gap-8">
    <dt aria-hidden="true" class="hidden">
        {$_("task-screen.task-title")}
    </dt>
    <dd>
        <TaskUpdateTitle title={task.title} readonly />
    </dd>
    <dt aria-hidden="true" class="hidden">
        {$_("task-screen.assignee")}
    </dt>
    <dd>
        <TaskUpdateUser workspaceUser={task.assignee || null} />
    </dd>
    <dt aria-hidden="true" class="hidden">
        {$_("task-screen.labels")}
    </dt>
    <dd>
        <TaskUpdateLabel labels={task.labels} />
    </dd>
    <dt aria-hidden="true" class="hidden">
        {$_("task-screen.section")}
    </dt>
    <dd>
        <TaskUpdateSection {task} />
    </dd>
</dl>
