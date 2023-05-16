<script lang="ts">
    import { _ } from "svelte-i18n";
    import SectionBar from "$lib/figma/cards/SectionBar.svelte";
    import {
        createCurrentSearchedTasks,
        currentWorkspaceBoardSections,
        taskSearchInput,
    } from "$lib/stores/dashboard";

    import TaskCard from "$lib/figma/cards/TaskCard.svelte";
    import type { WorkspaceBoard } from "$lib/types/workspace";
    import {
        createMoveTaskModule,
        createWorkspaceBoardSectionModule,
    } from "$lib/stores/modules";

    import FloatingActionButton from "$lib/figma/buttons/FloatingActionButton.svelte";
    import { openConstructiveOverlay } from "$lib/stores/globalUi";

    export let workspaceBoard: WorkspaceBoard;

    const currentSearchedTasks = createCurrentSearchedTasks(
        currentWorkspaceBoardSections,
        taskSearchInput
    );

    function onAddNewSection() {
        openConstructiveOverlay(
            {
                kind: "createWorkspaceBoardSection",
                workspaceBoard,
            },
            {
                kind: "sync",
                action: () => {
                    console.error("NOOP XXX");
                },
            }
        );
    }
</script>

<div class="relative flex h-full min-h-full grow flex-col bg-base-200">
    {#if $currentSearchedTasks}
        <!-- Flat Tasks Results -->
        {#if $currentSearchedTasks.length}
            <div class="flex grow flex-col overflow-y-auto p-2">
                {#each $currentSearchedTasks as task}
                    <TaskCard {task} moveTaskModule={undefined} />
                {/each}
            </div>
        {:else}
            <div class="flex grow items-center justify-center">
                <div class="rounded-md bg-base-100 p-6 shadow-sm">
                    {$_("tasks-not-found-for")} "{$taskSearchInput}"
                </div>
            </div>
        {/if}
    {:else}
        <!-- Sections -->
        <div class="flex grow flex-col gap-16 overflow-y-auto p-2">
            {#each $currentWorkspaceBoardSections as workspaceBoardSection (workspaceBoardSection.uuid)}
                <SectionBar
                    {workspaceBoardSection}
                    {createMoveTaskModule}
                    workspaceBoardSectionModule={createWorkspaceBoardSectionModule(
                        $currentWorkspaceBoardSections,
                        workspaceBoardSection
                    )}
                />
            {/each}
        </div>
    {/if}
    <div class="absolute bottom-4 right-4">
        <FloatingActionButton icon="plus" action={onAddNewSection} />
    </div>
</div>
