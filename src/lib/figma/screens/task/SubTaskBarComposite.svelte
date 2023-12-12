<script lang="ts">
    // This is just for showing sub tasks
    import { _ } from "svelte-i18n";

    import SubTaskBar from "$lib/figma/screens/task/SubTaskBar.svelte";
    import SubTaskLine from "$lib/figma/screens/task/SubTaskLine.svelte";
    import type { SubTask } from "$lib/types/workspace";
    import { getSubTaskProgress } from "$lib/utils/workspace";

    export let subTasks: SubTask[] | undefined;
    export let onInteract: () => void;

    $: progress = subTasks && getSubTaskProgress(subTasks);
</script>

<SubTaskBar {progress} />
{#if subTasks && subTasks.length > 0}
    <div class="flex grow flex-col">
        {#each subTasks as subTask}
            <SubTaskLine {subTask} {onInteract} />
        {/each}
    </div>
{:else}
    {$_("task-screen.sub-tasks.empty-state-read-only")}
{/if}
