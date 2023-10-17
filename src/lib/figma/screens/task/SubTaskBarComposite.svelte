<script lang="ts">
    // This is just for showing sub tasks
    import { _ } from "svelte-i18n";

    import SubTaskC from "$lib/figma/buttons/SubTask.svelte";
    import SubTaskBar from "$lib/figma/screens/task/SubTaskBar.svelte";
    import type { SubTask } from "$lib/types/workspace";

    export let subTasks: SubTask[] | undefined;
    export let onInteract: () => void;

    const progress = 50;
</script>

<SubTaskBar {progress} />
{#if subTasks && subTasks.length > 0}
    <div class="flex grow flex-col">
        {#each subTasks as subTask}
            <SubTaskC {subTask} {onInteract} />
        {/each}
    </div>
{:else}
    {$_("task-screen.sub-tasks.empty-state-read-only")}
{/if}
