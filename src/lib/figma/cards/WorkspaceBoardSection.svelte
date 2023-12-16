<script lang="ts">
    // TODO rename me to WorkspaceBoardSection.svelte
    import { _ } from "svelte-i18n";

    import SectionTitle from "$lib/figma/cards/section-bar/SectionTitle.svelte";
    import TaskCard from "$lib/figma/cards/TaskCard.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { workspaceBoardSectionClosed } from "$lib/stores/dashboard";
    import type {
        WorkspaceBoardDetail,
        WorkspaceBoardSectionWithTasks,
    } from "$lib/types/workspace";
    import { getNewTaskUrl } from "$lib/urls";

    export let workspaceBoard: WorkspaceBoardDetail;
    export let workspaceBoardSection: WorkspaceBoardSectionWithTasks;

    const { uuid } = workspaceBoardSection;
    $: open = !$workspaceBoardSectionClosed.has(uuid);
</script>

<section class="flex flex-col">
    <SectionTitle {workspaceBoard} {workspaceBoardSection} {open} />
    {#if open}
        <div class="flex flex-col gap-2 rounded-b-2xl bg-foreground p-4">
            {#each workspaceBoardSection.tasks as task (task.uuid)}
                <TaskCard
                    {workspaceBoard}
                    task={{
                        ...task,
                        workspace_board_section: workspaceBoardSection,
                    }}
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
        </div>
    {/if}
</section>
