<script lang="ts">
    import ProfileContextMenu from "$lib/figma/overlays/context-menu/ProfileContextMenu.svelte";
    import WorkspaceContextMenu from "$lib/figma/overlays/context-menu/WorkspaceContextMenu.svelte";
    import SideNavContextMenu from "$lib/figma/overlays/context-menu/SideNavContextMenu.svelte";
    import WorkspaceBoardContextMenu from "$lib/figma/overlays/context-menu/WorkspaceBoardContextMenu.svelte";
    import WorkspaceBoardSectionContextMenu from "$lib/figma/overlays/context-menu/WorkspaceBoardSectionContextMenu.svelte";
    import TaskContextMenu from "$lib/figma/overlays/context-menu/TaskContextMenu.svelte";
    import HelpContextMenu from "$lib/figma/overlays/context-menu/HelpContextMenu.svelte";
    import PermissionsContextMenu from "$lib/figma/overlays/context-menu/PermissionsContextMenu.svelte";
    import UpdateMemberOverlay from "$lib/figma/overlays/UpdateMemberOverlay.svelte";
    import UpdateLabelOverlay from "$lib/figma/overlays/UpdateLabelOverlay.svelte";
    import type { ContextMenuType } from "$lib/types/ui";

    export let target: ContextMenuType;
</script>

<div
    class="flex w-60 flex-col rounded-lg border border-border bg-foreground py-2 shadow-context-menu"
>
    {#if target.kind === "profile"}
        <ProfileContextMenu />
    {:else if target.kind === "workspace"}
        <WorkspaceContextMenu
            workspaceSearchModule={target.workspaceSearchModule}
        />
    {:else if target.kind === "sideNav"}
        <SideNavContextMenu
            workspace={target.workspace}
            sideNavModule={target.sideNavModule}
        />
    {:else if target.kind === "workspaceBoard"}
        <WorkspaceBoardContextMenu workspaceBoard={target.workspaceBoard} />
    {:else if target.kind === "workspaceBoardSection"}
        <WorkspaceBoardSectionContextMenu
            workspaceBoardSection={target.workspaceBoardSection}
            workspaceBoardSectionModule={target.workspaceBoardSectionModule}
        />
    {:else if target.kind === "task"}
        <TaskContextMenu task={target.task} location={target.location} />
    {:else if target.kind === "help"}
        <HelpContextMenu />
    {:else if target.kind === "permissions"}
        <PermissionsContextMenu />
    {:else if target.kind === "updateMember"}
        <UpdateMemberOverlay
            workspaceUserSearchModule={target.workspaceUserSearchModule}
        />
    {:else if target.kind === "updateLabel"}
        <UpdateLabelOverlay labelSearchModule={target.labelSearchModule} />
    {/if}
</div>
