<script lang="ts">
    import { _ } from "svelte-i18n";

    import SubTaskBar from "$lib/figma/screens/task/SubTaskBar.svelte";
    import SubTaskLine from "$lib/figma/screens/task/SubTaskLine.svelte";
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
            <SubTaskLine
                bind:subTask
                readonly={false}
                {index}
                {subTaskAssignment}
            />
        {/each}
    </div>
{:else}
    {$_("task-screen.sub-tasks.empty-state")}
{/if}
