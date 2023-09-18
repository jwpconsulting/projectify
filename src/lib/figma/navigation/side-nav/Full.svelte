<script lang="ts">
    import WorkspaceMenu from "$lib/figma/buttons/WorkspaceMenu.svelte";
    import LabelDropdown from "$lib/figma/composites/LabelDropdown.svelte";
    import Boards from "$lib/figma/navigation/side-nav/Boards.svelte";
    import Members from "$lib/figma/navigation/side-nav/Members.svelte";
    import type {
        LabelSearchModule,
        WorkspaceUserSearchModule,
    } from "$lib/types/stores";
    import type { Workspace } from "$lib/types/workspace";

    export let workspaces: Workspace[];
    export let workspace: Workspace;
    export let labelSearchModule: LabelSearchModule;
    export let workspaceUserSearchModule: WorkspaceUserSearchModule;
</script>

<nav class="flex h-full shrink-0 flex-col bg-base-100 py-4 pr-px">
    <WorkspaceMenu {workspaces} {workspace} open={true} />
    <div class="flex flex-col overflow-x-auto overflow-y-scroll">
        <Boards {workspace} />
        <Members {workspaceUserSearchModule} />
        <LabelDropdown {labelSearchModule} />
    </div>
</nav>
