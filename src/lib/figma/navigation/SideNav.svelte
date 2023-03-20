<script lang="ts">
    import WorkspaceMenu from "$lib/figma/buttons/WorkspaceMenu.svelte";
    import Boards from "$lib/figma/navigation/side-nav/Boards.svelte";
    import Members from "$lib/figma/navigation/side-nav/Members.svelte";
    import FilterLabelCollapsible from "$lib/figma/composites/FilterLabelCollapsible.svelte";
    import type { WorkspaceUserSearchModule } from "$lib/types/stores";

    import {
        currentWorkspace,
        selectWorkspaceUser,
        deselectWorkspaceUser,
        selectedWorkspaceUser,
        tasksPerUser,
        workspaceUserSearch,
        workspaceUserSearchResults,
    } from "$lib/stores/dashboard";

    const workspaceUserSearchModule: WorkspaceUserSearchModule = {
        select: selectWorkspaceUser,
        deselect: deselectWorkspaceUser,
        selected: selectedWorkspaceUser,
        tasksPerUser,
        search: workspaceUserSearch,
        searchResults: workspaceUserSearchResults,
    };
</script>

<nav class="flex h-full w-72 shrink-0 flex-col bg-base-100 py-4 pr-px">
    <WorkspaceMenu />
    <div class="flex flex-col overflow-x-auto overflow-y-scroll">
        <Boards {currentWorkspace} />
        <Members {workspaceUserSearchModule} />
        <FilterLabelCollapsible />
    </div>
</nav>
