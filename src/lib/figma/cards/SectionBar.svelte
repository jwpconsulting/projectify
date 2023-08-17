<script lang="ts">
    import { _ } from "svelte-i18n";

    import { getNewTaskUrl } from "$lib/urls";

    import SectionTitle from "$lib/figma/cards/section-bar/SectionTitle.svelte";
    import TaskCard from "$lib/figma/cards/TaskCard.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { workspaceBoardSectionClosed } from "$lib/stores/dashboard";
    import type {
        Task,
        WorkspaceBoard,
        WorkspaceBoardSection,
    } from "$lib/types/workspace";

    export let workspaceBoard: WorkspaceBoard;
    export let workspaceBoardSection: WorkspaceBoardSection;

    const { uuid } = workspaceBoardSection;
    $: open = !$workspaceBoardSectionClosed.has(uuid);

    let tasks: Task[] = [];
    $: tasks = open ? workspaceBoardSection.tasks ?? [] : [];
</script>

<div class="flex flex-col">
    <SectionTitle {workspaceBoard} {workspaceBoardSection} {open} />
    {#if open}
        <main class="flex flex-col gap-2 rounded-b-2xl bg-foreground p-4">
            {#each tasks as task, inx (task.uuid)}
                <TaskCard
                    {workspaceBoardSection}
                    {tasks}
                    {task}
                    isFirst={inx === 0}
                    isLast={inx === tasks.length - 1}
                />
            {:else}
                <p>
                    {$_("dashboard.section.empty.message")}
                    <Anchor
                        label={$_("dashboard.section.empty.prompt")}
                        size="normal"
                        href={getNewTaskUrl(workspaceBoardSection.uuid)}
                    />
                </p>
            {/each}
        </main>
    {/if}
</div>
