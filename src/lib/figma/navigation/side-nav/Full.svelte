<script lang="ts">
    import WorkspaceMenu from "$lib/figma/buttons/WorkspaceMenu.svelte";
    import Boards from "$lib/figma/navigation/side-nav/Boards.svelte";
    import FilterLabels from "$lib/figma/navigation/side-nav/FilterLabels.svelte";
    import WorkspaceUsers from "$lib/figma/navigation/side-nav/WorkspaceUsers.svelte";
    import { showFilters } from "$lib/stores/dashboard";
    import type { Workspace } from "$lib/types/workspace";

    export let workspaces: Workspace[];
    export let workspace: Workspace;
</script>

<!-- XXX temporary fix to alleviate long side nav inside mobile menu -->
<nav class="flex flex-col py-4">
    <WorkspaceMenu {workspaces} {workspace} open={true} />
    <div class="flex shrink flex-col overflow-x-auto overflow-y-scroll">
        <Boards {workspace} />
        {#if $showFilters}
            <WorkspaceUsers />
            <FilterLabels />
        {/if}
    </div>
</nav>
