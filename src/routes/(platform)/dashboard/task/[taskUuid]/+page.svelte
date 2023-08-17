<script lang="ts">
    import TaskReadCard from "$lib/figma/screens/task/TaskReadCard.svelte";
    import { currentTask } from "$lib/stores/dashboard";
</script>

{#if $currentTask}
    <TaskReadCard task={$currentTask} />
{/if}
