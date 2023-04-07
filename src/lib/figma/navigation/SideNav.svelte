<script lang="ts">
    import WorkspaceMenu from "$lib/figma/buttons/WorkspaceMenu.svelte";
    import Boards from "$lib/figma/navigation/side-nav/Boards.svelte";
    import Members from "$lib/figma/navigation/side-nav/Members.svelte";
    import LabelDropdown from "$lib/figma/composites/LabelDropdown.svelte";
    import type {
        LabelSearchModule,
        SideNavModule,
        WorkspaceBoardSearchModule,
        WorkspaceUserSearchModule,
    } from "$lib/types/stores";

    export let workspaceBoardSearchModule: WorkspaceBoardSearchModule;
    export let workspaceUserSearchModule: WorkspaceUserSearchModule;
    export let labelSearchModule: LabelSearchModule;
    export let sideNavModule: SideNavModule;

    let { showWorkspaceContextMenu, showSideNavContextMenu } = sideNavModule;
</script>

<nav class="flex h-full w-72 shrink-0 flex-col bg-base-100 py-4 pr-px">
    <WorkspaceMenu {showWorkspaceContextMenu} {showSideNavContextMenu} />
    <div class="flex flex-col overflow-x-auto overflow-y-scroll">
        <Boards {workspaceBoardSearchModule} />
        <Members {workspaceUserSearchModule} />
        <LabelDropdown {labelSearchModule} />
    </div>
</nav>
