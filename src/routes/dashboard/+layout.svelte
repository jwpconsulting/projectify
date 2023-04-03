<script lang="ts">
    import AuthGuard from "$lib/components/AuthGuard.svelte";
    import HeaderDashboard from "$lib/figma/navigation/header/Dashboard.svelte";
    import SideNav from "$lib/figma/navigation/SideNav.svelte";
    import { openContextMenu } from "$lib/stores/global-ui";

    import type {
        WorkspaceSearchModule,
        WorkspaceBoardSearchModule,
        WorkspaceUserSearchModule,
        LabelSearchModule,
        SideNavModule,
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
        sideNavOpen,
        toggleSideNavOpen,
        setWorkspaces,
    } from "$lib/stores/dashboard";

    import { user } from "$lib/stores/user";

    const workspaceSearchModule: WorkspaceSearchModule = {
        workspaces,
        currentWorkspace,
        setWorkspaces,
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

    let sideNavModule: SideNavModule;
    $: sideNavModule = {
        sideNavOpen,
        toggleSideNavOpen,
        showWorkspaceContextMenu: (anchor: HTMLElement) => {
            openContextMenu(
                { kind: "workspace", workspaceSearchModule },
                anchor
            );
        },
        showSideNavContextMenu: (anchor: HTMLElement) => {
            if (!$currentWorkspace) {
                throw new Error("Expected $currentWorkspace");
            }
            openContextMenu(
                {
                    kind: "sideNav",
                    workspace: $currentWorkspace,
                    // XXX circular reference, not cool Justus 2023-03-30
                    sideNavModule,
                },
                anchor
            );
        },
    };
</script>

<AuthGuard>
    <div class="flex h-screen flex-col">
        {#if $user}
            <HeaderDashboard user={$user} />
        {/if}
        <div class="flex grow flex-row">
            <SideNav
                {workspaceBoardSearchModule}
                {workspaceUserSearchModule}
                {labelSearchModule}
                {sideNavModule}
            />
            <slot />
        </div>
    </div>
</AuthGuard>
