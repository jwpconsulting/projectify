<script lang="ts">
    import ProfileContextMenu from "$lib/figma/overlays/context-menu/ProfileContextMenu.svelte";
    import WorkspaceContextMenu from "$lib/figma/overlays/context-menu/WorkspaceContextMenu.svelte";
    import SideNavContextMenu from "$lib/figma/overlays/context-menu/SideNavContextMenu.svelte";
    import WorkspaceBoardContextMenu from "$lib/figma/overlays/context-menu/WorkspaceBoardContextMenu.svelte";
    import WorkspaceBoardSectionContextMenu from "$lib/figma/overlays/context-menu/WorkspaceBoardSectionContextMenu.svelte";
    import TaskContextMenu from "$lib/figma/overlays/context-menu/TaskContextMenu.svelte";
    import HelpContextMenu from "$lib/figma/overlays/context-menu/HelpContextMenu.svelte";
    import PermissionsContextMenu from "$lib/figma/overlays/context-menu/PermissionsContextMenu.svelte";
    import { workspaces } from "$lib/stores/dashboard";
    import type { ContextMenuType } from "$lib/types/ui";
    import type { WorkspaceSearchModule } from "$lib/types/stores";

    export let target: ContextMenuType;

    const workspaceSearchModule: WorkspaceSearchModule = {
        workspaces,
    };
</script>

<div
    class="flex w-60 flex-col rounded-lg border border-border py-2 shadow-context-menu"
>
    {#if target.kind === "profile"}
        <ProfileContextMenu />
    {:else if target.kind === "workspace"}
        <WorkspaceContextMenu {workspaceSearchModule} />
    {:else if target.kind === "sideNav"}
        <SideNavContextMenu workspace={target.workspace} />
    {:else if target.kind === "workspaceBoard"}
        <WorkspaceBoardContextMenu workspaceBoard={target.workspaceBoard} />
    {:else if target.kind === "workspaceBoardSection"}
        <WorkspaceBoardSectionContextMenu
            workspaceBoardSection={target.workspaceBoardSection}
        />
    {:else if target.kind === "task"}
        <TaskContextMenu task={target.task} location={target.location} />
    {:else if target.kind === "help"}
        <HelpContextMenu />
    {:else if target.kind === "permissions"}
        <PermissionsContextMenu />
    {/if}
</div>
