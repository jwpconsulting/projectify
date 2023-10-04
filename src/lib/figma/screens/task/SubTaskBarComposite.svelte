<script lang="ts">
    // This is just for showing sub tasks
    import SubTaskC from "$lib/figma/buttons/SubTask.svelte";
    import SubTaskBar from "$lib/figma/screens/task/SubTaskBar.svelte";
    import type { SubTask } from "$lib/types/workspace";

    export let subTasks: SubTask[] | undefined;

    const progress = 50;
</script>

<SubTaskBar {progress} />
{#if subTasks && subTasks.length > 0}
    <div class="flex grow flex-col">
        {#each subTasks as subTask}
            <SubTaskC {subTask} />
        {/each}
    </div>
{:else}
    TODO no sub tasks
{/if}
