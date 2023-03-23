<script lang="ts">
    import WorkspaceMenu from "$lib/figma/buttons/WorkspaceMenu.svelte";
    import Boards from "$lib/figma/navigation/side-nav/Boards.svelte";
    import Members from "$lib/figma/navigation/side-nav/Members.svelte";
    import LabelDropdown from "$lib/figma/composites/LabelDropdown.svelte";
    import type {
        WorkspaceBoardSearchModule,
        WorkspaceUserSearchModule,
        LabelSearchModule,
    } from "$lib/types/stores";

    // TODO we might want to put the modules inside lib/stores
    export let workspaceBoardSearchModule: WorkspaceBoardSearchModule;
    export let workspaceUserSearchModule: WorkspaceUserSearchModule;
    export let labelSearchModule: LabelSearchModule;
</script>

<nav class="flex h-full w-72 shrink-0 flex-col bg-base-100 py-4 pr-px">
    <WorkspaceMenu />
    <div class="flex flex-col overflow-x-auto overflow-y-scroll">
        <Boards {workspaceBoardSearchModule} />
        <Members {workspaceUserSearchModule} />
        <LabelDropdown {labelSearchModule} />
    </div>
</nav>
