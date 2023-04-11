<script lang="ts">
    import TaskScreenMobile from "$lib/figma/screens/task/TaskScreenMobile.svelte";
    import TaskScreenDesktop from "$lib/figma/screens/task/TaskScreenDesktop.svelte";
    import type { TaskOrNewTask } from "$lib/types/ui";

    export let taskOrNewTask: TaskOrNewTask;
</script>

<div class="block lg:hidden">
    <TaskScreenMobile {taskOrNewTask} />
</div>
<div class="hidden lg:block">
    <TaskScreenDesktop {taskOrNewTask} />
</div>
