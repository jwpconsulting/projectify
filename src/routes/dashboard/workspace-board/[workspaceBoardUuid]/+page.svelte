<script lang="ts">
    import Loading from "$lib/components/loading.svelte";
    import Dashboard from "$lib/components/dashboard/Dashboard.svelte";
    import { page } from "$app/stores";
    import SideNav from "$lib/figma/navigation/SideNav.svelte";
    import { createLabel as repositoryCreateLabel } from "$lib/repository/workspace";

    import { openContextMenu } from "$lib/stores/global-ui";

    import type {
        LabelSearchModule,
        SideNavModule,
        WorkspaceBoardSearchModule,
        WorkspaceSearchModule,
        WorkspaceUserSearchModule,
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
        setWorkspaces,
        sideNavOpen,
        tasksPerUser,
        toggleSideNavOpen,
        workspaceUserSearch,
        workspaceUserSearchResults,
        workspaces,
    } from "$lib/stores/dashboard";

    $: {
        $currentWorkspaceBoardUuid = $page.params["workspaceBoardUuid"];
        console.log($currentWorkspaceBoardUuid);
    }

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

    let labelSearchModule: LabelSearchModule;
    // XXX
    // Again, we need to make this using a factory thing somewhere
    // Otherwise we duplicate code in 3 different locations (task creation,
    // side nav, task updating)
    // Justus 2023-05-02
    $: labelSearchModule = {
        select: selectLabel,
        deselect: deselectLabel,
        selected: selectedLabels,
        search: labelSearch,
        searchResults: labelSearchResults,
        async createLabel(color: number, name: string) {
            if (!$currentWorkspace) {
                throw new Error("Expected $currentWorkspace");
            }
            await repositoryCreateLabel($currentWorkspace, name, color);
        },
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

{#if $currentWorkspaceBoard}
    <div class="flex grow flex-row">
        <SideNav
            {workspaceBoardSearchModule}
            {workspaceUserSearchModule}
            {labelSearchModule}
            {sideNavModule}
        />
        <Dashboard workspaceBoard={$currentWorkspaceBoard} />
    </div>
{:else}
    <Loading />
{/if}
