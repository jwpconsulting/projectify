<script lang="ts">
    import ReadTaskCard from "$lib/figma/screens/task/ReadTaskCard.svelte";
    import { currentTask } from "$lib/stores/dashboard";
</script>

{#if $currentTask}
    <ReadTaskCard task={$currentTask} />
{/if}
