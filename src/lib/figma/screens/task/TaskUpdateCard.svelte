<script lang="ts">
    import TaskScreenMobile from "$lib/figma/screens/task/TaskScreenMobile.svelte";
    import TaskScreenDesktop from "$lib/figma/screens/task/TaskScreenDesktop.svelte";
    import type { Task } from "$lib/types/workspace";

    export let task: Task;
</script>

<div class="block lg:hidden">
    <TaskScreenMobile {task} />
</div>
<div class="hidden lg:block">
    <TaskScreenDesktop {task} />
</div>
