<script lang="ts">
    import TaskC from "$lib/components/dashboard/task/Task.svelte";
    import TaskUpdateBar from "$lib/figma/buttons/TaskUpdateBar.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import UpdateTaskFormFields from "$lib/figma/screens/task/UpdateTaskFormFields.svelte";
    import type { TaskUpdateBarState } from "$lib/figma/types";
    import type { TaskModule } from "$lib/types/stores";
    import type { Task } from "$lib/types/workspace";

    export let task: Task;
    export let taskModule: TaskModule;
    export let state: TaskUpdateBarState = "task";

    $: taskOrNewTask = { kind: "task" as const, task };
</script>

<TaskC>
    <TopBar slot="top-bar" {taskOrNewTask} {taskModule} />
    <TaskUpdateBar slot="tab-bar-mobile" kind="mobile" {state} {task} />
    <TaskUpdateBar slot="tab-bar-desktop" kind="mobile" {state} {task} />
    <UpdateTaskFormFields slot="content" {task} {taskModule} />
</TaskC>
