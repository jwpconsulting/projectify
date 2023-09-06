<script lang="ts">
    import { _ } from "svelte-i18n";

    import CreateWorkspaceBoard from "$lib/figma/overlays/constructive/CreateWorkspaceBoard.svelte";
    import InviteMember from "$lib/figma/overlays/constructive/InviteMember.svelte";
    import InviteMemberError from "$lib/figma/overlays/constructive/InviteMemberError.svelte";
    import NewWorkspace from "$lib/figma/overlays/constructive/NewWorkspace.svelte";
    import NewWorkspaceBoardSection from "$lib/figma/overlays/constructive/NewWorkspaceBoardSection.svelte";
    import RecoverWorkspaceBoard from "$lib/figma/overlays/constructive/RecoverWorkspaceBoard.svelte";
    import SkipOnboarding from "$lib/figma/overlays/constructive/SkipOnboarding.svelte";
    import UpdateWorkspaceBoard from "$lib/figma/overlays/constructive/UpdateWorkspaceBoard.svelte";
    import type { ConstructiveOverlayType } from "$lib/types/ui";

    export let target: ConstructiveOverlayType;
    $: title = {
        updateWorkspaceBoard: $_("edit-workspace-board.title"),
        createWorkspaceBoard: $_("new-workspace-board.title"),
        inviteTeamMembers: $_("invite-member.title"),
        inviteTeamMembersNoSeatsLeft: $_("invite-member-error.title"),
        createWorkspaceBoardSection: $_("new-workspace-board-section.title"),
        createWorkspace: $_("new-workspace.title"),
        skipOnboarding: $_("skip-onboarding.title"),
        recoverWorkspaceBoard: $_("recover-workspace-board.title"),
    }[target.kind];
</script>

<div class="flex max-w-lg grow flex-col gap-10 rounded-lg bg-foreground p-8">
    <div class="text-center text-3xl font-bold">
        {title}
    </div>
    <form class="flex flex-col gap-8">
        {#if target.kind === "updateWorkspaceBoard"}
            <UpdateWorkspaceBoard workspaceBoard={target.workspaceBoard} />
        {:else if target.kind === "createWorkspaceBoard"}
            <CreateWorkspaceBoard workspace={target.workspace} />
        {:else if target.kind === "inviteTeamMembers"}
            <InviteMember workspace={target.workspace} />
        {:else if target.kind === "inviteTeamMembersNoSeatsLeft"}
            <InviteMemberError workspace={target.workspace} />
        {:else if target.kind === "createWorkspaceBoardSection"}
            <NewWorkspaceBoardSection workspaceBoard={target.workspaceBoard} />
        {:else if target.kind === "createWorkspace"}
            <NewWorkspace />
        {:else if target.kind === "skipOnboarding"}
            <SkipOnboarding />
        {:else if target.kind === "recoverWorkspaceBoard"}
            <RecoverWorkspaceBoard workspaceBoard={target.workspaceBoard} />
        {/if}
    </form>
</div>
