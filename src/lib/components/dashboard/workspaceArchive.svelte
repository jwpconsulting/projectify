<script lang="ts">
    import { page } from "$app/stores";
    import {
        Mutation_ArchiveWorkspaceBoard,
        Mutation_DeleteWorkspaceBoard,
        Query_ArchivedWorkspaceBoards,
    } from "$lib/graphql/operations";
    import { query } from "svelte-apollo";
    import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";
    import debounce from "lodash/debounce.js";
    import { dateStringToLocal } from "$lib/utils/date";
    import DialogModal, { getModal } from "$lib/components/dialogModal.svelte";
    import ConfirmModalContent from "$lib/components/confirmModalContent.svelte";
    import { _ } from "svelte-i18n";
    import { client } from "$lib/graphql/client";

    $: workspaceUUID = $page.params["workspaceUUID"];

    let res = null;
    let workspaceWSStore;
    let workspace = null;
    let archivedBoards = [];

    const refetch = debounce(() => {
        res.refetch();
    }, 100);
    $: {
        if (workspaceUUID) {
            res = query(Query_ArchivedWorkspaceBoards, {
                variables: { uuid: workspaceUUID },
                fetchPolicy: "network-only",
            });

            workspaceWSStore = getSubscriptionForCollection(
                "workspace",
                workspaceUUID
            );
        }
    }

    $: {
        if ($workspaceWSStore) {
            refetch();
        }
    }

    $: {
        if (res && $res.data) {
            workspace = $res.data["workspace"];
            if (workspace["archivedBoards"]) {
                archivedBoards = workspace["archivedBoards"];
            }
        }
    }

    let unarchivingItems = {};

    async function onUnarchiveItem(item) {
        let uuid = item.uuid;

        unarchivingItems[uuid] = true;
        try {
            await client.mutate({
                mutation: Mutation_ArchiveWorkspaceBoard,
                variables: {
                    input: {
                        uuid: uuid,
                        archived: false,
                    },
                },
                update(cache, { data }) {
                    cache.modify({
                        id: `Workspace:${workspaceUUID}`,
                        fields: {
                            archivedBoards(list = []) {
                                return list.filter(
                                    (it) =>
                                        it.__ref != `WorkspaceBoard:${uuid}`
                                );
                            },
                        },
                    });
                },
            });
        } catch (error) {
            console.error(error);
        }
        unarchivingItems[uuid] = false;
    }

    async function onDeleteItem(item) {
        let uuid = item.uuid;
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

            // TODO: don't refetch when server notification work on delete mutation
            res.refetch();
        } catch (error) {
            console.error(error);
        }
    }
</script>

<div class="divide-y divide-base-300 p-4">
    {#if archivedBoards.length > 0}
        {#each archivedBoards as board}
            <div class="flex py-4 space-x-2">
                <div class="grid grow">
                    <div class="overflow-hidden nowrap-ellipsis">
                        <span class="font-bold nowrap-ellipsis"
                            >{board.title}</span
                        >
                    </div>
                    <div class="text-xs">
                        {dateStringToLocal(board.archived)}
                    </div>
                </div>
                <div
                    class="flex space-x-2 justify-center items-center shrink-0"
                >
                    <button
                        class:loading={unarchivingItems[board.uuid]}
                        on:click={() => {
                            onUnarchiveItem(board);
                        }}
                        class="btn text-primary btn-sm btn-ghost btn-primary rounded-full"
                        >Return</button
                    >
                    <button
                        on:click={() => {
                            onDeleteItem(board);
                        }}
                        class="btn btn-accent btn-sm btn-outline rounded-full"
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

<DialogModal id="deleteArchivedBoard">
    <ConfirmModalContent
        title={"Delete Archive"}
        confirmLabel={$_("Delete")}
        confirmColor="accent"
    >
        {"Deleted archive cannot be returned. Would you like to delete this archive?"}
    </ConfirmModalContent>
</DialogModal>
