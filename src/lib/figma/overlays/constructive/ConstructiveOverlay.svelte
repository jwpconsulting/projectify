<script lang="ts">
    import CreateWorkspace from "$lib/figma/overlays/constructive/CreateWorkspace.svelte";
    import CreateWorkspaceBoard from "$lib/figma/overlays/constructive/CreateWorkspaceBoard.svelte";
    import CreateWorkspaceBoardSection from "$lib/figma/overlays/constructive/CreateWorkspaceBoardSection.svelte";
    import InviteWorkspaceUser from "$lib/figma/overlays/constructive/InviteWorkspaceUser.svelte";
    import InviteWorkspaceUserError from "$lib/figma/overlays/constructive/InviteWorkspaceUserError.svelte";
    import RecoverWorkspaceBoard from "$lib/figma/overlays/constructive/RecoverWorkspaceBoard.svelte";
    import SkipOnboarding from "$lib/figma/overlays/constructive/SkipOnboarding.svelte";
    import UpdateWorkspaceBoard from "$lib/figma/overlays/constructive/UpdateWorkspaceBoard.svelte";
    import type { ConstructiveOverlayType } from "$lib/types/ui";

    import UpdateWorkspaceBoardSection from "./UpdateWorkspaceBoardSection.svelte";

    export let target: ConstructiveOverlayType;
</script>

{#if target.kind === "updateWorkspaceBoard"}
    <UpdateWorkspaceBoard workspaceBoard={target.workspaceBoard} />
{:else if target.kind === "createWorkspaceBoard"}
    <CreateWorkspaceBoard workspace={target.workspace} />
{:else if target.kind === "inviteWorkspaceUser"}
    <InviteWorkspaceUser workspace={target.workspace} />
{:else if target.kind === "inviteWorkspaceUserError"}
    <InviteWorkspaceUserError workspace={target.workspace} />
{:else if target.kind === "createWorkspaceBoardSection"}
    <CreateWorkspaceBoardSection workspaceBoard={target.workspaceBoard} />
{:else if target.kind === "updateWorkspaceBoardSection"}
    <UpdateWorkspaceBoardSection
        workspaceBoardSection={target.workspaceBoardSection}
    />
{:else if target.kind === "createWorkspace"}
    <CreateWorkspace />
{:else if target.kind === "skipOnboarding"}
    <SkipOnboarding />
{:else if target.kind === "recoverWorkspaceBoard"}
    <RecoverWorkspaceBoard workspaceBoard={target.workspaceBoard} />
{/if}
