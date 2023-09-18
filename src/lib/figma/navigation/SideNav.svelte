<script lang="ts">
    import Collapsed from "$lib/figma/navigation/side-nav/Collapsed.svelte";
    import Full from "$lib/figma/navigation/side-nav/Full.svelte";
    import { createLabel as repositoryCreateLabel } from "$lib/repository/workspace";
    import {
        createLabelSearch,
        createLabelSearchResults,
        currentWorkspaceLabels,
        deselectLabel,
        selectLabel,
        selectedLabels,
        sideNavOpen,
        createTasksPerUser,
        currentWorkspaceBoardSections,
        deselectWorkspaceUser,
        selectWorkspaceUser,
        selectedWorkspaceUser,
        workspaceUserSearch,
        workspaceUserSearchResults,
    } from "$lib/stores/dashboard";
    import type {
        LabelSearchModule,
        WorkspaceUserSearchModule,
    } from "$lib/types/stores";
    import type { Workspace } from "$lib/types/workspace";

    export let workspaces: Workspace[];
    export let workspace: Workspace;

    let workspaceUserSearchModule: WorkspaceUserSearchModule;
    $: workspaceUserSearchModule = {
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

{#if $sideNavOpen}
    <div class="max-w-xs 2xl:max-w-md">
        <Full
            {workspaces}
            {workspace}
            {workspaceUserSearchModule}
            {labelSearchModule}
        />
    </div>
{:else}
    <!-- Figma says 72px but we only have 64 or 80 (16, 29 rem respectively)-->
    <!-- Might we refactor this into something separate? -->
    <div class="w-20">
        <Collapsed
            {workspace}
            {workspaces}
            {workspaceUserSearchModule}
            {labelSearchModule}
        />
    </div>
{/if}
