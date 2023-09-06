<script lang="ts">
    import type { PageData } from "../$types";

    import TaskC from "$lib/components/dashboard/task/Task.svelte";
    import TaskUpdateBar from "$lib/figma/buttons/TaskUpdateBar.svelte";
    import TaskUpdates from "$lib/figma/screens/task/TaskUpdates.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import type { TaskUpdateBarState } from "$lib/figma/types";
    import { currentTask } from "$lib/stores/dashboard";

    export let data: PageData;
    let { task } = data;
    const { workspaceBoardSection } = data;

    export let state: TaskUpdateBarState = "updates";

    $: task = $currentTask ?? task;
</script>

<TaskC>
    <TopBar slot="top-bar" breadcrumb={{ task, workspaceBoardSection }} />
    <TaskUpdates slot="content" />
    <!-- TODO dry this up with the thing above -->
    <TaskUpdateBar slot="tab-bar-mobile" kind="mobile" {state} {task} />
    <TaskUpdateBar slot="tab-bar-desktop" kind="mobile" {state} {task} />
</TaskC>
