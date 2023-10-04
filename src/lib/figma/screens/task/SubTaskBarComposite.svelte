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
    <div class="flex flex-col">
        {#each subTasks as subTask}
            <SubTaskC
                createOrUpdateSubTask={{ kind: "update", update: subTask }}
                state="normal"
            />
        {/each}
    </div>
{:else}
    TODO no sub tasks
{/if}
