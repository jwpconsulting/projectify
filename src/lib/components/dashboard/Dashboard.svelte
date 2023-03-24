<script lang="ts">
    import Board from "$lib/components/dashboard/board.svelte";
    import {
        closeTaskDetails,
        currentWorkspace,
        currentWorkspaceBoard,
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
        workspaces,
    } from "$lib/stores/dashboard";

    import { page } from "$app/stores";
    import { onMount } from "svelte";
    import { _ } from "svelte-i18n";
    import SideNav from "$lib/figma/navigation/SideNav.svelte";

    import type {
        WorkspaceSearchModule,
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

    const workspaceSearchModule: WorkspaceSearchModule = {
        workspaces,
        currentWorkspace,
    };

    const workspaceBoardSearchModule: WorkspaceBoardSearchModule = {
        currentWorkspace,
        currentWorkspaceBoard,
        currentWorkspaceBoardUuid,
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
        {workspaceSearchModule}
        {workspaceBoardSearchModule}
        {workspaceUserSearchModule}
        {labelSearchModule}
    />
    <div class="flex h-full grow overflow-y-auto">
        <Board />
    </div>
</div>
