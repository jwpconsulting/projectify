<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import TaskCard from "$lib/figma/cards/TaskCard.svelte";
    import SectionTitle from "$lib/figma/cards/section-bar/SectionTitle.svelte";
    import type { Task, WorkspaceBoardSection } from "$lib/types/workspace";
    import { createMoveTaskModule } from "$lib/stores/modules";

    export let section: WorkspaceBoardSection;

    const dispatch = createEventDispatcher();

    let open = true;

    function toggleOpen() {
        open = !open;
    }

    let tasks: Task[] = [];
    $: {
        if (open && section.tasks) {
            tasks = section.tasks;
        } else {
            tasks = [];
        }
    }

    // TODO Turn these into props
    function switchWithPrevSection({ detail }: { detail: unknown }) {
        dispatch("switchWithPrevSection", detail);
    }

    function switchWithNextSection({ detail }: { detail: unknown }) {
        dispatch("switchWithNextSection", detail);
    }
</script>

<div class="flex flex-col">
    <SectionTitle
        {section}
        {toggleOpen}
        bind:open
        on:switchWithPrevSection={switchWithPrevSection}
        on:switchWithNextSection={switchWithNextSection}
    />
    <main class="flex flex-col gap-2 rounded-b-2xl bg-foreground p-4">
        {#each tasks as task, inx (task.uuid)}
            <TaskCard
                workspaceBoardSection={section}
                {task}
                isFirst={inx === 0}
                isLast={inx === tasks.length - 1}
                moveTaskModule={createMoveTaskModule(section, task, tasks)}
            />
        {/each}
    </main>
</div>
