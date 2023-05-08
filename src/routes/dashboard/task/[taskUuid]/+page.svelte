<script lang="ts">
    import { currentTask } from "$lib/stores/dashboard";
    import TaskReadCard from "$lib/figma/screens/task/TaskReadCard.svelte";
</script>

{#if $currentTask}
    <TaskReadCard task={$currentTask} />
{/if}
