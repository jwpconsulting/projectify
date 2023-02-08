<script lang="ts">
    import BoardSection from "./board-section.svelte";
    import {
        Mutation_AddWorkspaceBoardSection,
        Mutation_MoveWorkspaceBoardSection,
    } from "$lib/graphql/operations";
    import IconPlus from "../icons/icon-plus.svelte";
    import { getModal } from "../dialogModal.svelte";
    import { client } from "$lib/graphql/client";
    import { _ } from "svelte-i18n";
    import {
        currentWorkspaceBoard,
        currentWorkspaceBoardUuid,
        currentWorkspaceBoardSections,
        currentSearchedTasks,
        taskSearchInput,
    } from "$lib/stores/dashboard";

    import TaskCard from "$lib/components/dashboard/TaskCard.svelte";
    import Loading from "../loading.svelte";
    import type { WorkspaceBoardSection } from "$lib/types/workspace";

    async function onAddNewSection() {
        let modalRes = await getModal("newBoardSectionModal").open();
        if (modalRes?.confirm) {
            try {
                const newSection = {
                    title: modalRes.outputs.title,
                    description: "",
                };
                await client.mutate({
                    mutation: Mutation_AddWorkspaceBoardSection,
                    variables: {
                        input: {
                            workspaceBoardUuid: $currentWorkspaceBoardUuid,
                            ...newSection,
                        },
                    },
                    optimisticResponse: {
                        addWorkspaceBoardSection: {
                            uuid: "temp-id",
                            __typename: "WorkspaceBoardSection",
                            ...newSection,
                            created: "",
                            tasks: [],
                        },
                    },
                });
            } catch (error) {
                console.error(error);
            }
        }
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
            <div
                class="section-layout-row flex grow flex-col overflow-y-auto p-2"
            >
                {#each $currentWorkspaceBoardSections as section, index (section.uuid)}
                    <BoardSection
                        {section}
                        isFirst={index == 0}
                        isLast={index ==
                            $currentWorkspaceBoardSections.length - 1}
                        on:switchWithPrevSection={onSwitchWithPrevSection}
                        on:switchWithNextSection={onSwitchWithNextSection}
                    />
                {/each}
                <div
                    class="ignore-elements m-2 flex shrink-0 space-x-4 bg-base-100 p-5 font-bold text-primary shadow-sm hover:cursor-pointer hover:ring"
                    on:click={() => onAddNewSection()}
                    on:keydown={() => onAddNewSection()}
                >
                    <IconPlus />
                    <div>{$_("new-section")}</div>
                </div>
            </div>
        {/if}
    </div>
{/if}

<style lang="scss">
    .section-layout-row {
        @apply flex-col;
    }
</style>
