<script lang="ts">
    import { _ } from "svelte-i18n";
    import type { ConstructiveOverlayType } from "$lib/types";
    import EditWorkspaceBoard from "$lib/figma/EditWorkspaceBoard.svelte";
    import NewWorkspaceBoard from "$lib/figma/NewWorkspaceBoard.svelte";
    import InviteMember from "$lib/figma/InviteMember.svelte";
    import InviteMemberError from "$lib/figma/InviteMemberError.svelte";
    import NewWorkspaceBoardSection from "$lib/figma/NewWorkspaceBoardSection.svelte";
    import NewWorkspace from "$lib/figma/NewWorkspace.svelte";
    import SkipOnboarding from "$lib/figma/SkipOnboarding.svelte";
    import RecoverWorkspaceBoard from "$lib/figma/RecoverWorkspaceBoard.svelte";

    export let target: ConstructiveOverlayType;
    $: title = {
        updateWorkspaceBoard: $_("constructive-overlay.please-edit-me-please"),
        createWorkspaceBoard: $_("constructive-overlay.please-edit-me-please"),
        inviteTeamMembers: $_("constructive-overlay.please-edit-me-please"),
        inviteTeamMembersNoSeatsLeft: $_(
            "constructive-overlay.please-edit-me-please"
        ),
        createWorkspaceBoardSection: $_(
            "constructive-overlay.please-edit-me-please"
        ),
        createWorkspace: $_("constructive-overlay.please-edit-me-please"),
        skipOnboarding: $_("constructive-overlay.please-edit-me-please"),
        recoverWorkspaceBoard: $_(
            "constructive-overlay.please-edit-me-please"
        ),
    }[target.kind];
</script>

<div class="flex flex-col gap-10 p-8">
    <div class="text-center text-3xl font-bold">
        {title}
    </div>
    <form class="flex flex-col gap-8">
        {#if target.kind === "updateWorkspaceBoard"}
            <EditWorkspaceBoard workspaceBoard={target.workspaceBoard} />
        {:else if target.kind === "createWorkspaceBoard"}
            <NewWorkspaceBoard workspace={target.workspace} />
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
