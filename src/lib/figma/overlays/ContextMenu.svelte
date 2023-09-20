<script lang="ts">
    import HelpContextMenu from "$lib/figma/overlays/context-menu/HelpContextMenu.svelte";
    import Permissions from "$lib/figma/overlays/context-menu/Permissions.svelte";
    import Profile from "$lib/figma/overlays/context-menu/Profile.svelte";
    import SideNavContextMenu from "$lib/figma/overlays/context-menu/SideNavContextMenu.svelte";
    import Task from "$lib/figma/overlays/context-menu/Task.svelte";
    import Workspace from "$lib/figma/overlays/context-menu/Workspace.svelte";
    import WorkspaceBoard from "$lib/figma/overlays/context-menu/WorkspaceBoard.svelte";
    import WorkspaceBoardSectionContextMenu from "$lib/figma/overlays/context-menu/WorkspaceBoardSectionContextMenu.svelte";
    import UpdateLabelOverlay from "$lib/figma/overlays/UpdateLabelOverlay.svelte";
    import UpdateMemberOverlay from "$lib/figma/overlays/UpdateMemberOverlay.svelte";
    import type { ContextMenuType } from "$lib/types/ui";

    export let target: ContextMenuType;
</script>

{#if target.kind === "profile"}
    <Profile />
{:else if target.kind === "workspace"}
    <Workspace workspaces={target.workspaces} />
{:else if target.kind === "sideNav"}
    <SideNavContextMenu workspace={target.workspace} />
{:else if target.kind === "workspaceBoard"}
    <WorkspaceBoard workspaceBoard={target.workspaceBoard} />
{:else if target.kind === "workspaceBoardSection"}
    <WorkspaceBoardSectionContextMenu
        workspaceBoard={target.workspaceBoard}
        workspaceBoardSection={target.workspaceBoardSection}
    />
{:else if target.kind === "task"}
    <Task
        task={target.task}
        location={target.location}
        moveTaskModule={target.moveTaskModule}
        workspaceBoardSection={target.workspaceBoardSection}
    />
{:else if target.kind === "help"}
    <HelpContextMenu />
{:else if target.kind === "permissions"}
    <Permissions />
{:else if target.kind === "updateMember"}
    <UpdateMemberOverlay
        workspaceUserAssignment={target.workspaceUserAssignment}
    />
{:else if target.kind === "updateLabel"}
    <UpdateLabelOverlay labelAssignment={target.labelAssignment} />
{/if}
