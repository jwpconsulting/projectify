<script lang="ts">
    import type { PageData } from "./$types";

    import Dashboard from "$lib/components/dashboard/Dashboard.svelte";
    import SideNav from "$lib/figma/navigation/SideNav.svelte";
    import {
        createTasksPerUser,
        currentWorkspace,
        currentWorkspaceBoard,
        currentWorkspaceBoardSections,
        deselectWorkspaceUser,
        selectWorkspaceUser,
        selectedWorkspaceUser,
        workspaceUserSearch,
        workspaceUserSearchResults,
    } from "$lib/stores/dashboard";
    import type { WorkspaceUserSearchModule } from "$lib/types/stores";

    export let data: PageData;

    let { workspaceBoard, workspace, workspaces } = data;

    $: workspaceBoard = $currentWorkspaceBoard ?? workspaceBoard;
    $: workspace = $currentWorkspace ?? workspace;

    let workspaceUserSearchModule: WorkspaceUserSearchModule;
    $: workspaceUserSearchModule = {
        select: selectWorkspaceUser,
        deselect: deselectWorkspaceUser,
        selected: selectedWorkspaceUser,
        tasksPerUser: createTasksPerUser(currentWorkspaceBoardSections),
        search: workspaceUserSearch,
        searchResults: workspaceUserSearchResults,
    };
</script>

<div class="flex h-full grow flex-row">
    <SideNav {workspaces} {workspace} {workspaceUserSearchModule} />
    <Dashboard {workspaceBoard} />
</div>
