<script lang="ts">
    import {
        currentWorkspaceBoardUuid,
        openTaskDetails,
    } from "$lib/stores/dashboard";
    import { _ } from "svelte-i18n";
    import TaskCard from "$lib/figma/cards/TaskCard.svelte";
    import SectionTitle from "$lib/figma/cards/section-bar/SectionTitle.svelte";
    import { createEventDispatcher } from "svelte";
    import type { WorkspaceBoardSection, Task } from "$lib/types/workspace";

    export let section: WorkspaceBoardSection;

    export let isFirst: boolean | null = null;
    export let isLast: boolean | null = null;

    const dispatch = createEventDispatcher();

    let open: boolean = true;

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

    function switchWithPrevSection({ detail }: { detail: any }) {
        dispatch("switchWithPrevSection", detail);
    }

    function switchWithNextSection({ detail }: { detail: any }) {
        dispatch("switchWithNextSection", detail);
    }
</script>

<div class="flex flex-col">
    <SectionTitle
        {isLast}
        {isFirst}
        {section}
        {toggleOpen}
        bind:open
        on:switchWithPrevSection={switchWithPrevSection}
        on:switchWithNextSection={switchWithNextSection}
    />
    <main class="flex flex-col gap-2">
        {#each tasks as task, inx (task.uuid)}
            <TaskCard
                workspaceBoardSection={section}
                {task}
                isFirst={inx === 0}
                isLast={inx === tasks.length - 1}
                on:click={() => {
                    if (!$currentWorkspaceBoardUuid) {
                        throw new Error("Expected $currentWorkspaceBoardUuid");
                    }
                    openTaskDetails($currentWorkspaceBoardUuid, task.uuid);
                }}
            />
        {/each}
    </main>
</div>
