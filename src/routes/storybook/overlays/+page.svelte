<script lang="ts">
    import { onMount } from "svelte";

    import {
        fc,
        task,
        workspace,
        workspaceBoard,
        workspaceBoardSection,
        workspaceUser,
    } from "$lib/storybook";

    import { browser } from "$app/environment";
    import ConstructiveOverlay from "$lib/figma/overlays/constructive/ConstructiveOverlay.svelte";
    import DestructiveOverlay from "$lib/figma/overlays/DestructiveOverlay.svelte";
    import { setFirstWorkspace } from "$lib/stores/dashboard";
    import type {
        ConstructiveOverlayType,
        DestructiveOverlayType,
    } from "$lib/types/ui";

    const destructiveOverlays: DestructiveOverlayType[] = [
        {
            kind: "deleteLabel" as const,
            label: { name: "This is a label", color: 0, uuid: "" },
        },
        {
            kind: "deleteMember" as const,
            workspaceUser,
        },
        {
            kind: "deleteSection" as const,
            workspaceBoardSection,
        },
        {
            kind: "deleteTask" as const,
            task,
        },
        {
            kind: "deleteSelectedTasks" as const,
            tasks: [task],
        },
        {
            kind: "archiveBoard" as const,
            workspaceBoard: {
                title: "board name",
                created: "",
                modified: "",
                uuid: "",
            },
        },
        {
            kind: "deleteBoard" as const,
            workspaceBoard,
        },
    ];

    const constructiveOverlays: ConstructiveOverlayType[] = [
        { kind: "updateWorkspaceBoard", workspaceBoard },
        { kind: "createWorkspaceBoard", workspace },
        { kind: "inviteTeamMembers", workspace },
        { kind: "inviteTeamMembersNoSeatsLeft", workspace },
        {
            kind: "createWorkspaceBoardSection",
            workspaceBoard,
        },
        { kind: "createWorkspace" },
        { kind: "skipOnboarding" },
        { kind: "recoverWorkspaceBoard", workspaceBoard },
    ];
    onMount(async () => {
        if (browser) {
            await setFirstWorkspace();
        }
    });
</script>

{#each destructiveOverlays as target}
    <DestructiveOverlay {target} />
{/each}

<div class={fc}>
    {#each constructiveOverlays as target}
        <div class="w-[500px]">
            <ConstructiveOverlay {target} />
        </div>
    {/each}
</div>
