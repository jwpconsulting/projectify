<script lang="ts">
    import Board from "$lib/components/dashboard/board.svelte";
    import DrawerModal from "$lib/components/drawerModal.svelte";
    import TaskDetails from "$lib/components/dashboard/task-details.svelte";
    import {
        closeTaskDetails,
        currentWorkspace,
        currentWorkspaceBoardUuid,
        deselectLabel,
        deselectWorkspaceUser,
        drawerModalOpen,
        labelSearch,
        labelSearchResults,
        selectLabel,
        selectWorkspaceUser,
        selectedLabels,
        selectedWorkspaceUser,
        tasksPerUser,
        workspaceUserSearch,
        workspaceUserSearchResults,
    } from "$lib/stores/dashboard";
    import DialogModal from "$lib/components/dialogModal.svelte";

    import { page } from "$app/stores";
    import { onMount } from "svelte";
    import ConfirmModalContent from "$lib/components/confirmModalContent.svelte";
    import { _ } from "svelte-i18n";
    import SideNav from "$lib/figma/navigation/SideNav.svelte";

    import type {
        WorkspaceBoardSearchModule,
        WorkspaceUserSearchModule,
        LabelSearchModule,
    } from "$lib/types/stores";

    let selectedWorkspaceUuid: string | null;
    let selectedTaskUuid: string | null;
    $: {
        $currentWorkspaceBoardUuid = $page.params["workspaceBoardUuid"];
    }

    $: {
        if (
            !$drawerModalOpen &&
            selectedWorkspaceUuid &&
            $currentWorkspaceBoardUuid &&
            selectedTaskUuid
        ) {
            closeTaskDetails();
        }
    }

    onMount(() => {});

    const workspaceBoardSearchModule: WorkspaceBoardSearchModule = {
        currentWorkspace,
    };
    const workspaceUserSearchModule: WorkspaceUserSearchModule = {
        select: selectWorkspaceUser,
        deselect: deselectWorkspaceUser,
        selected: selectedWorkspaceUser,
        tasksPerUser,
        search: workspaceUserSearch,
        searchResults: workspaceUserSearchResults,
    };

    const labelSearchModule: LabelSearchModule = {
        select: selectLabel,
        deselect: deselectLabel,
        selected: selectedLabels,
        search: labelSearch,
        searchResults: labelSearchResults,
    };
</script>

<div class="flex grow flex-row divide-x divide-base-300 overflow-hidden">
    <SideNav
        {workspaceBoardSearchModule}
        {workspaceUserSearchModule}
        {labelSearchModule}
    />
    <div class="flex h-full grow overflow-y-auto">
        <Board />
    </div>
</div>

<DrawerModal bind:open={$drawerModalOpen}>
    <TaskDetails />
</DrawerModal>

<DialogModal id="newBoardModal">
    <ConfirmModalContent
        title={$_("new-workspace-board")}
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
        inputs={[
            {
                name: "title",
                label: $_("section-name"),
                validation: { required: true },
            },
        ]}
    />
</DialogModal>

<DialogModal id="editBoardSectionModal">
    <ConfirmModalContent
        title={$_("edit-section")}
        confirmLabel={$_("Save")}
        inputs={[
            {
                name: "title",
                label: $_("section-name"),
                validation: { required: true },
            },
        ]}
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
