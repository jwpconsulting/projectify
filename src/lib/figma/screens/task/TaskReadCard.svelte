<script lang="ts">
    import TaskUpdateBar from "$lib/figma/buttons/TaskUpdateBar.svelte";
    import TaskFields from "$lib/figma/screens/task/TaskFields.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import TaskC from "$lib/components/dashboard/task/Task.svelte";
    import type { Task } from "$lib/types/workspace";
    import type { TaskUpdateBarState } from "$lib/figma/types";

    export let task: Task;
    export let state: TaskUpdateBarState = "task";

    $: taskOrNewTask = { kind: "task" as const, task };
</script>

<TaskC>
    <TopBar slot="top-bar" {taskOrNewTask} taskModule={null} />
    <TaskFields slot="content" {task} />
    <TaskUpdateBar slot="tab-bar-mobile" kind="mobile" {state} {task} />
    <TaskUpdateBar slot="tab-bar-desktop" kind="mobile" {state} {task} />
</TaskC>
