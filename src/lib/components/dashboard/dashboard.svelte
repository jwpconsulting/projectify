<script lang="ts">
    import WorkspacesSideNav from "$lib/components/dashboard/workspaces-side-nav.svelte";
    import BoardsSideNav from "$lib/components/dashboard/boards-side-nav.svelte";
    import Board from "./board.svelte";
    import IconSettings from "../icons/icon-settings.svelte";
    import DrawerModal from "../drawerModal.svelte";
    import TaskDetails from "./task-details.svelte";
    import {
        currentWorkspaceUUID,
        currentBoardUUID,
        drawerModalOpen,
        closeTaskDetails,
        openTaskDetails,
    } from "$lib/stores/dashboard";
    import DialogModal from "../dialogModal.svelte";
    import NewBoardModal from "./newBoardModal.svelte";
    import NewBoardSectionModal from "./newBoardSectionModal.svelte";

    import { page } from "$app/stores";
    import { decodeUUID } from "$lib/utils/encoders";
    import { onMount } from "svelte";
    import ConfirmModalContent from "../confirmModalContent.svelte";
    import { _ } from "svelte-i18n";

    $: uuids = $page.params["uuids"].split("/");

    $: selectedWorkspaceUUID = uuids[0] ? decodeUUID(uuids[0]) : null;
    $: selectedBoardUUID = uuids[1] ? decodeUUID(uuids[1]) : null;
    $: selectedTaskUUID = uuids[2] ? decodeUUID(uuids[2]) : null;

    $: {
        currentWorkspaceUUID.set(selectedWorkspaceUUID);
        currentBoardUUID.set(selectedBoardUUID);
    }

    $: {
        if (
            !$drawerModalOpen &&
            selectedWorkspaceUUID &&
            selectedBoardUUID &&
            selectedTaskUUID
        ) {
            closeTaskDetails();
        }
    }

    onMount(() => {
        if (selectedTaskUUID) {
            openTaskDetails(selectedTaskUUID);
        }
    });
</script>

<main
    class="page p-0 flex-row divide-x divide-base-300 select-none bg-base-200"
>
    <!-- First side bar -->
    <WorkspacesSideNav bind:selectedWorkspaceUUID />

    <!-- Secon side bar -->
    <nav
        class="flex flex-col bg-base-100 w-60 h-min min-h-screen sticky top-0"
    >
        <!-- Tite and settings -->
        <div class="flex p-4 sticky top-0 bg-base-100">
            <h1 class="grow font-bold text-xl">Projectify</h1>
            <button class="btn btn-primary btn-outline btn-circle btn-xs">
                <IconSettings />
            </button>
        </div>

        <!-- Boards nav -->
        <div class="flex flex-col grow">
            {#if selectedWorkspaceUUID}
                <h2 class="p-4 text-base font-bold">Workspace Boards</h2>
                <BoardsSideNav {selectedWorkspaceUUID} {selectedBoardUUID} />
            {/if}
        </div>

        <!-- User infos -->
        <div class="flex p-3 sticky bottom-0 bg-base-100">
            <div
                class="m-1 flex -space-x-1 overflow-hidden w-8 h-8 rounded-full shrink-0"
            >
                <img
                    width="100%"
                    height="100%"
                    src="https://picsum.photos/200"
                    alt="user"
                />
            </div>
            <div class="m-1 overflow-hidden">
                <div
                    class="text-xs overflow-hidden whitespace-nowrap text-ellipsis"
                >
                    Interface Designer & Frontend Interface Designer
                </div>
                <div
                    class="text-base font-bold overflow-hidden whitespace-nowrap text-ellipsis"
                >
                    Abraham
                </div>
            </div>
        </div>
    </nav>

    <Board bind:boardUUID={selectedBoardUUID} />

    <DrawerModal bind:open={$drawerModalOpen}>
        <TaskDetails />
    </DrawerModal>

    <DialogModal id="newBoardModal">
        <NewBoardModal />
    </DialogModal>

    <DialogModal id="newBoardSectionModal">
        <NewBoardSectionModal />
    </DialogModal>

    <DialogModal id="deleteBoardSectionConfirmModal">
        <ConfirmModalContent
            title={$_("delete-section")}
            confirmLabel={$_("Delete")}
        >
            {$_(
                "deleted-section-cannot-be-returned-would-you-like-to-delete-this-section"
            )}
        </ConfirmModalContent>
    </DialogModal>
</main>
