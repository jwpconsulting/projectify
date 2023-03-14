<script lang="ts">
    import {
        Mutation_ArchiveWorkspaceBoard,
        Mutation_DeleteWorkspaceBoard,
    } from "$lib/graphql/operations";
    import { dateStringToLocal } from "$lib/utils/date";
    import DialogModal, { getModal } from "$lib/components/dialogModal.svelte";
    import ConfirmModalContent from "$lib/components/confirmModalContent.svelte";
    import { _ } from "svelte-i18n";
    import { client } from "$lib/graphql/client";
    import Loading from "$lib/components/loading.svelte";
    import type { WorkspaceBoard } from "$lib/types/workspace";
    import { currentArchivedWorkspaceBoards } from "$lib/stores/dashboard";

    const unarchivingItems = new Map<string, boolean>();
    let loading: boolean;

    $: {
        console.log($currentArchivedWorkspaceBoards);
        loading = !$currentArchivedWorkspaceBoards;
    }

    async function onUnarchiveItem(item: WorkspaceBoard) {
        let uuid = item.uuid;

        unarchivingItems.set(uuid, true);
        try {
            await client.mutate({
                mutation: Mutation_ArchiveWorkspaceBoard,
                variables: {
                    input: {
                        uuid: uuid,
                        archived: false,
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
        unarchivingItems.set(uuid, false);
    }

    async function onDeleteItem(item: WorkspaceBoard) {
        let modalRes = await getModal("deleteArchivedBoard").open();

        if (!modalRes) {
            return;
        }

        try {
            await client.mutate({
                mutation: Mutation_DeleteWorkspaceBoard,
                variables: {
                    input: {
                        uuid: item.uuid,
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
    }
</script>

{#if loading}
    <div class="flex min-h-[200px] items-center justify-center">
        <Loading />
    </div>
{:else}
    <div class="divide-y divide-base-300 p-4">
        {#if $currentArchivedWorkspaceBoards.length > 0}
            {#each $currentArchivedWorkspaceBoards as workspaceBoard}
                <div class="flex space-x-2 py-4">
                    <div class="grid grow">
                        <div class="nowrap-ellipsis overflow-hidden">
                            <span class="nowrap-ellipsis font-bold"
                                >{workspaceBoard.title}</span
                            >
                        </div>
                        <div class="text-xs">
                            {workspaceBoard.archived
                                ? dateStringToLocal(workspaceBoard.archived)
                                : null}
                        </div>
                    </div>
                    <div
                        class="flex shrink-0 items-center justify-center space-x-2"
                    >
                        <button
                            class:loading={unarchivingItems.get(
                                workspaceBoard.uuid
                            )}
                            on:click={() => {
                                onUnarchiveItem(workspaceBoard);
                            }}
                            class="btn btn-primary btn-ghost btn-sm rounded-full text-primary"
                            >Return</button
                        >
                        <button
                            on:click={() => {
                                onDeleteItem(workspaceBoard);
                            }}
                            class="btn btn-outline btn-accent btn-sm rounded-full"
                            >Delete</button
                        >
                    </div>
                </div>
            {/each}
        {:else}
            <div class="text-center text-gray-600">
                {$_("no-archived-boards-found")}
            </div>
        {/if}
    </div>
{/if}

<DialogModal id="deleteArchivedBoard">
    <ConfirmModalContent
        title={"Delete Archive"}
        confirmLabel={$_("Delete")}
        confirmColor="accent"
    >
        {"Deleted archive cannot be returned. Would you like to delete this archive?"}
    </ConfirmModalContent>
</DialogModal>
