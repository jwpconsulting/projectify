<script lang="ts">
    import { _ } from "svelte-i18n";

    import SubTaskBar from "$lib/figma/screens/task/SubTaskBar.svelte";
    import SubTaskLine from "$lib/figma/screens/task/SubTaskLine.svelte";
    import type { SubTaskAssignment } from "$lib/types/stores";
    import { getSubTaskProgress } from "$lib/utils/workspace";

    export let subTaskAssignment: SubTaskAssignment;

    $: progress = getSubTaskProgress($subTaskAssignment);
    // What does the following TODO mean? Justus 2023-12-12
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
