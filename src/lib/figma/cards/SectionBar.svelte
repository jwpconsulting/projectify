<script lang="ts">
    import TaskCard from "$lib/figma/cards/TaskCard.svelte";
    import SectionTitle from "$lib/figma/cards/section-bar/SectionTitle.svelte";
    import type { Task, WorkspaceBoardSection } from "$lib/types/workspace";
    import type { createMoveTaskModule as _createMoveTaskModule } from "$lib/stores/modules";

    export let workspaceBoardSection: WorkspaceBoardSection;

    let open = true;

    function toggleOpen() {
        open = !open;
    }

    let tasks: Task[] = [];
    $: tasks = open ? workspaceBoardSection.tasks ?? [] : [];

    export let switchWithPrevSection: () => void;
    export let switchWithNextSection: () => void;
    export let createMoveTaskModule: typeof _createMoveTaskModule;
</script>

<div class="flex flex-col">
    <SectionTitle
        {workspaceBoardSection}
        {toggleOpen}
        bind:open
        on:switchWithPrevSection={switchWithPrevSection}
        on:switchWithNextSection={switchWithNextSection}
    />
    {#if tasks.length}
        <main class="flex flex-col gap-2 rounded-b-2xl bg-foreground p-4">
            {#each tasks as task, inx (task.uuid)}
                <TaskCard
                    {workspaceBoardSection}
                    {task}
                    isFirst={inx === 0}
                    isLast={inx === tasks.length - 1}
                    moveTaskModule={createMoveTaskModule(
                        workspaceBoardSection,
                        task,
                        tasks
                    )}
                />
            {/each}
        </main>
    {/if}
</div>
