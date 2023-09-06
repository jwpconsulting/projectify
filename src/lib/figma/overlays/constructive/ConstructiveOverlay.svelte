<script lang="ts">
    import { _ } from "svelte-i18n";

    import CreateWorkspace from "$lib/figma/overlays/constructive/CreateWorkspace.svelte";
    import CreateWorkspaceBoard from "$lib/figma/overlays/constructive/CreateWorkspaceBoard.svelte";
    import CreateWorkspaceBoardSection from "$lib/figma/overlays/constructive/CreateWorkspaceBoardSection.svelte";
    import InviteMember from "$lib/figma/overlays/constructive/InviteMember.svelte";
    import InviteMemberError from "$lib/figma/overlays/constructive/InviteMemberError.svelte";
    import Layout from "$lib/figma/overlays/constructive/Layout.svelte";
    import RecoverWorkspaceBoard from "$lib/figma/overlays/constructive/RecoverWorkspaceBoard.svelte";
    import SkipOnboarding from "$lib/figma/overlays/constructive/SkipOnboarding.svelte";
    import UpdateWorkspaceBoard from "$lib/figma/overlays/constructive/UpdateWorkspaceBoard.svelte";
    import type { ConstructiveOverlayType } from "$lib/types/ui";

    export let target: ConstructiveOverlayType;
    $: title = {
        updateWorkspaceBoard: $_(
            "overlay.constructive.update-workspace-board.title"
        ),
        createWorkspaceBoard: $_(
            "overlay.constructive.create-workspace-board.title"
        ),
        inviteTeamMembers: $_("overlay.constructive.invite-member.title"),
        inviteTeamMembersNoSeatsLeft: $_(
            "overlay.constructive.invite-member-error.title"
        ),
        createWorkspaceBoardSection: $_(
            "overlay.constructive.create-workspace-board-section.title"
        ),
        createWorkspace: $_("overlay.constructive.create-workspace.title"),
        skipOnboarding: $_("overlay.constructive.skip-onboarding.title"),
        recoverWorkspaceBoard: $_(
            "overlay.constructive.recover-workspace-board.title"
        ),
    }[target.kind];
</script>

<Layout>
    <svelte:fragment slot="title">
        {title}
    </svelte:fragment>>
    <svelte:fragment slot="form">
        {#if target.kind === "updateWorkspaceBoard"}
            <UpdateWorkspaceBoard workspaceBoard={target.workspaceBoard} />
        {:else if target.kind === "createWorkspaceBoard"}
            <CreateWorkspaceBoard workspace={target.workspace} />
        {:else if target.kind === "inviteTeamMembers"}
            <InviteMember workspace={target.workspace} />
        {:else if target.kind === "inviteTeamMembersNoSeatsLeft"}
            <InviteMemberError workspace={target.workspace} />
        {:else if target.kind === "createWorkspaceBoardSection"}
            <CreateWorkspaceBoardSection
                workspaceBoard={target.workspaceBoard}
            />
        {:else if target.kind === "createWorkspace"}
            <CreateWorkspace />
        {:else if target.kind === "skipOnboarding"}
            <SkipOnboarding />
        {:else if target.kind === "recoverWorkspaceBoard"}
            <RecoverWorkspaceBoard workspaceBoard={target.workspaceBoard} />
        {/if}
    </svelte:fragment>
</Layout>
