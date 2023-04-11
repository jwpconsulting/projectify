<script lang="ts">
    import Loading from "$lib/components/loading.svelte";
    import Dashboard from "$lib/components/dashboard/Dashboard.svelte";
    import { page } from "$app/stores";
    import SideNav from "$lib/figma/navigation/SideNav.svelte";

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
