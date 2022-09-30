<script lang="ts">
    import ProfileOverlay from "$lib/figma/ProfileOverlay.svelte";
    import WorkspaceOverlay from "$lib/figma/WorkspaceOverlay.svelte";
    import SideNavOverlay from "$lib/figma/SideNavOverlay.svelte";
    import WorkspaceBoardOverlay from "$lib/figma/WorkspaceBoardOverlay.svelte";
    import WorkspaceBoardSectionOverlay from "$lib/figma/WorkspaceBoardSectionOverlay.svelte";
    import TaskOverlay from "$lib/figma/TaskOverlay.svelte";
    import HelpOverlay from "$lib/figma/HelpOverlay.svelte";
    import PermissionsOverlay from "$lib/figma/PermissionsOverlay.svelte";
    import type { ContextMenuType } from "$lib/types/ui";

    export let target: ContextMenuType;
</script>

<div
    class="flex w-60 flex-col rounded-lg border border-border py-2 shadow-context-menu"
>
    {#if target.kind === "profile"}
        <ProfileOverlay />
    {:else if target.kind === "workspace"}
        <WorkspaceOverlay />
    {:else if target.kind === "sideNav"}
        <SideNavOverlay workspace={target.workspace} />
    {:else if target.kind === "workspaceBoard"}
        <WorkspaceBoardOverlay workspaceBoard={target.workspaceBoard} />
    {:else if target.kind === "workspaceBoardSection"}
        <WorkspaceBoardSectionOverlay
            workspaceBoardSection={target.workspaceBoardSection}
        />
    {:else if target.kind === "task"}
        <TaskOverlay task={target.task} location={target.location} />
    {:else if target.kind === "help"}
        <HelpOverlay />
    {:else if target.kind === "permissions"}
        <PermissionsOverlay />
    {/if}
</div>
