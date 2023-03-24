<script lang="ts">
    import AuthGuard from "$lib/components/authGuard.svelte";
    import HeaderDashboard from "$lib/figma/navigation/header/Dashboard.svelte";
    import SideNav from "$lib/figma/navigation/SideNav.svelte";

    import type {
        WorkspaceSearchModule,
        WorkspaceBoardSearchModule,
        WorkspaceUserSearchModule,
        LabelSearchModule,
    } from "$lib/types/stores";

    import {
        currentWorkspace,
        currentWorkspaceBoard,
        currentWorkspaceBoardUuid,
        deselectLabel,
        deselectWorkspaceUser,
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

    import { user } from "$lib/stores/user";

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

<AuthGuard>
    <div class="flex h-screen flex-col">
        {#if $user}
            <HeaderDashboard user={$user} />
        {/if}
        <div class="flex flex-row">
            <SideNav
                {workspaceSearchModule}
                {workspaceBoardSearchModule}
                {workspaceUserSearchModule}
                {labelSearchModule}
            />
            <slot />
        </div>
    </div>
</AuthGuard>
