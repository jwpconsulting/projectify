<script lang="ts">
    import SectionBar from "$lib/figma/cards/SectionBar.svelte";
    import { Mutation_MoveWorkspaceBoardSection } from "$lib/graphql/operations";
    import { client } from "$lib/graphql/client";
    import { _ } from "svelte-i18n";
    import {
        currentWorkspaceBoard,
        currentWorkspaceBoardSections,
        currentSearchedTasks,
        taskSearchInput,
    } from "$lib/stores/dashboard";

    import TaskCard from "$lib/figma/cards/TaskCard.svelte";
    import Loading from "$lib/components/loading.svelte";
    import type { WorkspaceBoardSection } from "$lib/types/workspace";

    import FloatingActionButton from "$lib/figma/buttons/FloatingActionButton.svelte";
    import { openConstructiveOverlay } from "$lib/stores/global-ui";

    function onAddNewSection() {
        // TODO ideally, we would be creating Dashboard with a workspaceBoard
        if (!$currentWorkspaceBoard) {
            throw new Error("Expected $currentWorkspaceBoard");
        }
        openConstructiveOverlay(
            {
                kind: "createWorkspaceBoardSection",
                workspaceBoard: $currentWorkspaceBoard,
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

    function onSwitchWithPrevSection({
        detail: { section },
    }: {
        detail: { section: WorkspaceBoardSection };
    }) {
        const sectionIndex = $currentWorkspaceBoardSections.findIndex(
            (s) => s.uuid == section.uuid
        );
        const prevSection = $currentWorkspaceBoardSections[sectionIndex - 1];

        if (prevSection) {
            moveSection(section.uuid, prevSection._order);
        }
    }
    function onSwitchWithNextSection({
        detail: { section },
    }: {
        detail: { section: WorkspaceBoardSection };
    }) {
        const sectionIndex: number = $currentWorkspaceBoardSections.findIndex(
            (s: WorkspaceBoardSection) => s.uuid == section.uuid
        );
        const nextSection: WorkspaceBoardSection | null =
            $currentWorkspaceBoardSections[sectionIndex + 1] || null;

        if (nextSection) {
            moveSection(section.uuid, nextSection._order);
        }
    }
</script>

{#if !$currentWorkspaceBoard}
    <div class="flex grow flex-col items-center justify-center bg-base-200">
        <Loading />
    </div>
{:else}
    <div class="relative flex h-full min-h-full grow flex-col bg-base-200">
        {#if $currentSearchedTasks}
            <!-- Flat Tasks Results -->
            {#if $currentSearchedTasks.length}
                <div class="flex grow flex-col overflow-y-auto p-2">
                    {#each $currentSearchedTasks as task}
                        <TaskCard {task} />
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
            <div class="flex grow flex-col overflow-y-auto p-2">
                {#each $currentWorkspaceBoardSections as section, index (section.uuid)}
                    <SectionBar
                        {section}
                        isFirst={index == 0}
                        isLast={index ==
                            $currentWorkspaceBoardSections.length - 1}
                        on:switchWithPrevSection={onSwitchWithPrevSection}
                        on:switchWithNextSection={onSwitchWithNextSection}
                    />
                {/each}
            </div>
        {/if}
        <div class="absolute bottom-4 right-4">
            <FloatingActionButton icon="plus" action={onAddNewSection} />
        </div>
    </div>
{/if}
