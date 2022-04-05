<script lang="ts">
    import Header from "$lib/components/Header.svelte";

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

    import { page } from "$app/stores";
    import { decodeUUID } from "$lib/utils/encoders";
    import { onMount } from "svelte";
    import ConfirmModalContent from "../confirmModalContent.svelte";
    import { _ } from "svelte-i18n";
    import IconMenu from "../icons/icon-menu.svelte";
    import IconArchive from "../icons/icon-archive.svelte";
    import DropDownMenu from "../dropDownMenu.svelte";

    export let selectedWorkspace = null;

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

<div class="flex grow flex-row divide-x divide-base-300 overflow-hidden">
    <!-- First side bar -->
    <WorkspacesSideNav bind:selectedWorkspaceUUID bind:selectedWorkspace />

    <!-- Secon side bar -->
    <nav
        class="sticky top-0 flex min-h-full w-60 shrink-0 flex-col bg-base-100"
    >
        <!-- Tite and settings -->
        <div class="sticky top-0 z-50 flex bg-base-100 p-4">
            <h1 class="grow text-xl font-bold capitalize">
                {selectedWorkspace ? selectedWorkspace.title : ""}
            </h1>
            <DropDownMenu
                items={[
                    {
                        label: $_("Archive"),
                        icon: IconArchive,
                        href: `/dashboard/archive/${selectedWorkspaceUUID}`,
                    },
                    {
                        label: $_("settings"),
                        icon: IconSettings,
                        href: `/dashboard/settings/${selectedWorkspaceUUID}`,
                    },
                ]}
            >
                <!-- svelte-ignore a11y-label-has-associated-control -->
                <label
                    tabindex="0"
                    class="btn btn-outline btn-primary btn-circle btn-xs"
                >
                    <IconMenu />
                </label>
            </DropDownMenu>
        </div>

        <!-- Boards nav -->
        <div class="flex grow flex-col overflow-hidden">
            {#if selectedWorkspaceUUID}
                <h2 class="p-4 text-base font-bold">Workspace Boards</h2>
                <BoardsSideNav {selectedWorkspaceUUID} {selectedBoardUUID} />
            {/if}
        </div>
    </nav>

    {#if selectedBoardUUID}
        <div class="flex h-full grow overflow-y-auto">
            <Board
                workspaceUUID={selectedWorkspaceUUID}
                bind:boardUUID={selectedBoardUUID}
            />
        </div>
    {/if}
</div>

<DrawerModal bind:open={$drawerModalOpen}>
    <TaskDetails />
</DrawerModal>

<DialogModal id="newBoardModal">
    <ConfirmModalContent
        title={$_("new-workspace-board")}
        confirmLabel={$_("Save")}
        inputs={[{ name: "title", label: $_("workspace-board-name") }]}
    />
</DialogModal>

<DialogModal id="editBoardModal">
    <ConfirmModalContent
        title={$_("edit-workspace-board")}
        confirmLabel={$_("Save")}
        inputs={[
            {
                name: "title",
                label: $_("workspace-board-name"),
                validation: { required: true },
            },
            {
                name: "deadline",
                label: $_("deadline"),
                type: "datePicker",
            },
        ]}
    />
</DialogModal>

<DialogModal id="newBoardSectionModal">
    <ConfirmModalContent
        title={$_("new-section")}
        confirmLabel={$_("Save")}
        inputs={[{ name: "title", label: $_("section-name") }]}
    />
</DialogModal>

<DialogModal id="editBoardSectionModal">
    <ConfirmModalContent
        title={$_("edit-section")}
        confirmLabel={$_("Save")}
        inputs={[{ name: "title", label: $_("section-name") }]}
    />
</DialogModal>

<DialogModal id="archiveBoardConfirmModal">
    <ConfirmModalContent
        title={$_("archive-board")}
        confirmLabel={$_("Archive")}
        confirmColor="accent"
    >
        {$_("archive-board-message")}
    </ConfirmModalContent>
</DialogModal>

<DialogModal id="deleteBoardConfirmModal">
    <ConfirmModalContent
        title={$_("delete-board")}
        confirmLabel={$_("Delete")}
        confirmColor="accent"
    >
        {$_("delete-board-message")}
    </ConfirmModalContent>
</DialogModal>

<DialogModal id="deleteBoardSectionConfirmModal">
    <ConfirmModalContent
        title={$_("delete-section")}
        confirmLabel={$_("Delete")}
        confirmColor="accent"
    >
        {$_(
            "deleted-section-cannot-be-returned-would-you-like-to-delete-this-section"
        )}
    </ConfirmModalContent>
</DialogModal>

<DialogModal id="deleteTaskConfirmModal">
    <ConfirmModalContent
        title={$_("delete-task")}
        confirmLabel={$_("Delete")}
        confirmColor="accent"
    >
        {$_("delete-task-modal-message")}
    </ConfirmModalContent>
</DialogModal>
