<script lang="ts">
    import type { PageData } from "./$types";
    import Dashboard from "$lib/components/dashboard/Dashboard.svelte";
    import SideNav from "$lib/figma/navigation/SideNav.svelte";
    import { createLabel as repositoryCreateLabel } from "$lib/repository/workspace";

    import type {
        LabelSearchModule,
        WorkspaceBoardSearchModule,
        WorkspaceUserSearchModule,
    } from "$lib/types/stores";

    import {
        createLabelSearch,
        createLabelSearchResults,
        createTasksPerUser,
        currentWorkspace,
        currentWorkspaceLabels,
        currentWorkspaceBoard,
        currentWorkspaceBoardSections,
        currentWorkspaceBoardUuid,
        deselectLabel,
        deselectWorkspaceUser,
        selectLabel,
        selectWorkspaceUser,
        selectedLabels,
        selectedWorkspaceUser,
        workspaceUserSearch,
        workspaceUserSearchResults,
    } from "$lib/stores/dashboard";

    export let data: PageData;

    let { workspaceBoard, workspace } = data;

    $: workspaceBoard = $currentWorkspaceBoard || workspaceBoard;
    $: workspace = $currentWorkspace || workspace;

    const workspaceBoardSearchModule: WorkspaceBoardSearchModule = {
        currentWorkspace,
        currentWorkspaceBoard,
        currentWorkspaceBoardUuid,
    };
    const workspaceUserSearchModule: WorkspaceUserSearchModule = {
        select: selectWorkspaceUser,
        deselect: deselectWorkspaceUser,
        selected: selectedWorkspaceUser,
        tasksPerUser: createTasksPerUser(currentWorkspaceBoardSections),
        search: workspaceUserSearch,
        searchResults: workspaceUserSearchResults,
    };

    let labelSearchModule: LabelSearchModule;
    // XXX
    // Again, we need to make this using a factory thing somewhere
    // Otherwise we duplicate code in 3 different locations (task creation,
    // side nav, task updating)
    // Justus 2023-05-02
    const labelSearch = createLabelSearch();
    $: labelSearchModule = {
        select: selectLabel,
        deselect: deselectLabel,
        selected: selectedLabels,
        search: labelSearch,
        searchResults: createLabelSearchResults(
            currentWorkspaceLabels,
            labelSearch
        ),
        async createLabel(color: number, name: string) {
            await repositoryCreateLabel(workspace, name, color);
        },
    };
</script>

<div class="flex grow flex-row">
    <SideNav
        {workspace}
        {workspaceBoardSearchModule}
        {workspaceUserSearchModule}
        {labelSearchModule}
    />
    <Dashboard {workspaceBoard} />
</div>
