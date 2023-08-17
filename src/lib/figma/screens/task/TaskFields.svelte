<script lang="ts">
    import TaskFieldsTemplate from "$lib/figma/screens/task/TaskFieldsTemplate.svelte";
    import TaskUpdateDescription from "$lib/figma/screens/task/TaskUpdateDescription.svelte";
    import TaskUpdateDueDate from "$lib/figma/screens/task/TaskUpdateDueDate.svelte";
    import TaskUpdateLabel from "$lib/figma/screens/task/TaskUpdateLabel.svelte";
    import TaskUpdateSection from "$lib/figma/screens/task/TaskUpdateSection.svelte";
    import TaskUpdateTitle from "$lib/figma/screens/task/TaskUpdateTitle.svelte";
    import TaskUpdateUser from "$lib/figma/screens/task/TaskUpdateUser.svelte";
    import type { Task } from "$lib/types/workspace";

    export let task: Task;
    // XXX refactor the dl dt dd structure into
    // src/lib/figma/screens/task/TaskFieldsTemplate.svelte
    // and add a slot for each form field thing
</script>

<TaskFieldsTemplate>
    <TaskUpdateTitle slot="title" title={task.title} readonly />
    <TaskUpdateUser slot="assignee" workspaceUser={task.assignee || null} />
    <TaskUpdateLabel slot="labels" labels={task.labels} />
    <TaskUpdateSection slot="section" {task} />
    <TaskUpdateDueDate slot="due-date" date={task.deadline || null} />
    <TaskUpdateDescription
        slot="description"
        readonly
        description={task.description}
    />
</TaskFieldsTemplate>
