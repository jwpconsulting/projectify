<script lang="ts">
    import TaskUpdateBar from "$lib/figma/buttons/TaskUpdateBar.svelte";
    import TaskFormFields from "$lib/figma/screens/task/TaskFormFields.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import TaskC from "$lib/components/dashboard/task/Task.svelte";
    import type { Task } from "$lib/types/workspace";
    import type { TaskUpdateBarState } from "$lib/figma/types";
    import type { TaskModule } from "$lib/types/stores";

    export let task: Task;
    export let taskModule: TaskModule;
    export let state: TaskUpdateBarState = "task";

    $: taskOrNewTask = { kind: "task" as const, task };
</script>

<TaskC>
    <TopBar slot="top-bar" {taskOrNewTask} {taskModule} />
    <TaskUpdateBar slot="tab-bar-mobile" kind="mobile" {state} {task} />
    <TaskUpdateBar slot="tab-bar-desktop" kind="mobile" {state} {task} />
    <TaskFormFields slot="content" {task} {taskModule} />
</TaskC>
