<script lang="ts">
    import SubTaskC from "$lib/figma/buttons/SubTask.svelte";
    import SubTaskBar from "$lib/figma/screens/task/SubTaskBar.svelte";
    import type { SubTaskAssignment } from "$lib/types/stores";

    export let subTaskAssignment: SubTaskAssignment;

    // TODO calculate progress
    const progress = 50;
    // TODO determine correct state for children. Or should they do that
    // themselves?
</script>

<SubTaskBar {progress} {subTaskAssignment} />
{#if $subTaskAssignment.length > 0}
    <div class="flex flex-col">
        {#each $subTaskAssignment as subTask, index}
            <SubTaskC
                bind:subTask
                readonly={false}
                {index}
                {subTaskAssignment}
            />
        {/each}
    </div>
{:else}
    TODO no sub tasks
{/if}
