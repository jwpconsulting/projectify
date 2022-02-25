<script lang="ts">
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";
    import SettingPage from "$lib/components/settingPage.svelte";
    import { page } from "$app/stores";
    import { Query_ArchivedWorkspaceBoards } from "$lib/graphql/operations";
    import { query } from "svelte-apollo";
    import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";
    import debounce from "lodash/debounce.js";
    import { dateStringToLocal } from "$lib/utils/date";
    import AuthGuard from "$lib/components/authGuard.svelte";
    import DialogModal, { getModal } from "$lib/components/dialogModal.svelte";
    import ConfirmModalContent from "$lib/components/confirmModalContent.svelte";
    import { _ } from "svelte-i18n";

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

    async function onUnarchiveItem(uuid) {
        console.log("unarchive item", uuid);
    }

    async function onDeleteItem(uuid) {
        let modalRes = await getModal("deleteArchivedBoard").open();

        if (!modalRes) {
            return;
        }
    }
</script>

<PageLayout>
    <AuthGuard>
        <SettingPage title="Archives">
            <div class="divide-y divide-base-300 p-4">
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
                                on:click={() => {
                                    onUnarchiveItem(board.uuid);
                                }}
                                class="btn text-primary btn-sm btn-ghost btn-primary rounded-full"
                                >Return</button
                            >
                            <button
                                on:click={() => {
                                    onDeleteItem(board.uuid);
                                }}
                                class="btn btn-accent btn-sm btn-outline rounded-full"
                                >Delete</button
                            >
                        </div>
                    </div>
                {/each}
            </div>
        </SettingPage>
    </AuthGuard>
</PageLayout>

<DialogModal id="deleteArchivedBoard">
    <ConfirmModalContent
        title={"Delete Archive"}
        confirmLabel={$_("Delete")}
        confirmColor="accent"
    >
        {"Deleted archive cannot be returned. Would you like to delete this archive?"}
    </ConfirmModalContent>
</DialogModal>
