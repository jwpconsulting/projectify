<script lang="ts">
    import { _ } from "svelte-i18n";
    import SectionBar from "$lib/figma/cards/SectionBar.svelte";
    import { Mutation_MoveWorkspaceBoardSection } from "$lib/graphql/operations";
    import { client } from "$lib/graphql/client";
    import {
        createCurrentSearchedTasks,
        currentWorkspaceBoardSections,
        taskSearchInput,
    } from "$lib/stores/dashboard";

    import TaskCard from "$lib/figma/cards/TaskCard.svelte";
    import type {
        WorkspaceBoard,
        WorkspaceBoardSection,
    } from "$lib/types/workspace";
    import { createMoveTaskModule } from "$lib/stores/modules";

    import FloatingActionButton from "$lib/figma/buttons/FloatingActionButton.svelte";
    import { openConstructiveOverlay } from "$lib/stores/globalUi";
    import type { WorkspaceBoardSectionModule } from "$lib/types/stores";
    import {
        toggleWorkspaceBoardSectionOpen,
        workspaceBoardSectionClosed,
    } from "$lib/stores/dashboard/ui";

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

    async function moveSection(
        workspaceBoardSectionUuid: string,
        order: number
    ) {
        try {
            await client.mutate({
                mutation: Mutation_MoveWorkspaceBoardSection,
                variables: {
                    input: {
                        workspaceBoardSectionUuid,
                        order,
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
    }

    function switchWithPrevSection(section: WorkspaceBoardSection) {
        const sectionIndex = $currentWorkspaceBoardSections.findIndex(
            (s) => s.uuid == section.uuid
        );
        const prevSection = $currentWorkspaceBoardSections[sectionIndex - 1];

        if (prevSection) {
            moveSection(section.uuid, prevSection._order);
        }
    }
    function switchWithNextSection(section: WorkspaceBoardSection) {
        const sectionIndex: number = $currentWorkspaceBoardSections.findIndex(
            (s: WorkspaceBoardSection) => s.uuid == section.uuid
        );
        const nextSection: WorkspaceBoardSection | null =
            $currentWorkspaceBoardSections[sectionIndex + 1] || null;

        if (nextSection) {
            moveSection(section.uuid, nextSection._order);
        }
    }

    const workspaceBoardSectionModule: WorkspaceBoardSectionModule = {
        workspaceBoardSectionClosed,
        toggleWorkspaceBoardSectionOpen,
        switchWithPrevSection,
        switchWithNextSection,
    };
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
                    {workspaceBoardSectionModule}
                />
            {/each}
        </div>
    {/if}
    <div class="absolute bottom-4 right-4">
        <FloatingActionButton icon="plus" action={onAddNewSection} />
    </div>
</div>
