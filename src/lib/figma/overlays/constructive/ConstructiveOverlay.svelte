<script lang="ts">
    import CreateWorkspace from "$lib/figma/overlays/constructive/CreateWorkspace.svelte";
    import CreateWorkspaceBoard from "$lib/figma/overlays/constructive/CreateWorkspaceBoard.svelte";
    import CreateWorkspaceBoardSection from "$lib/figma/overlays/constructive/CreateWorkspaceBoardSection.svelte";
    import InviteMemberError from "$lib/figma/overlays/constructive/InviteMemberError.svelte";
    import InviteWorkspaceUser from "$lib/figma/overlays/constructive/InviteWorkspaceUser.svelte";
    import RecoverWorkspaceBoard from "$lib/figma/overlays/constructive/RecoverWorkspaceBoard.svelte";
    import SkipOnboarding from "$lib/figma/overlays/constructive/SkipOnboarding.svelte";
    import UpdateWorkspaceBoard from "$lib/figma/overlays/constructive/UpdateWorkspaceBoard.svelte";
    import type { ConstructiveOverlayType } from "$lib/types/ui";

    export let target: ConstructiveOverlayType;
</script>

{#if target.kind === "updateWorkspaceBoard"}
    <UpdateWorkspaceBoard workspaceBoard={target.workspaceBoard} />
{:else if target.kind === "createWorkspaceBoard"}
    <CreateWorkspaceBoard workspace={target.workspace} />
{:else if target.kind === "inviteTeamMembers"}
    <InviteWorkspaceUser workspace={target.workspace} />
{:else if target.kind === "inviteTeamMembersNoSeatsLeft"}
    <InviteMemberError workspace={target.workspace} />
{:else if target.kind === "createWorkspaceBoardSection"}
    <CreateWorkspaceBoardSection workspaceBoard={target.workspaceBoard} />
{:else if target.kind === "createWorkspace"}
    <CreateWorkspace />
{:else if target.kind === "skipOnboarding"}
    <SkipOnboarding />
{:else if target.kind === "recoverWorkspaceBoard"}
    <RecoverWorkspaceBoard workspaceBoard={target.workspaceBoard} />
{/if}
