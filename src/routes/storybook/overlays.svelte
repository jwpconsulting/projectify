<script lang="ts">
    import DestructiveOverlay from "$lib/figma/DestructiveOverlay.svelte";
    import ContextMenu from "$lib/figma/ContextMenu.svelte";
    import { setFirstWorkspace } from "$lib/stores/dashboard";
    import ConstructiveOverlay from "$lib/figma/ConstructiveOverlay.svelte";
    import type {
        ContextMenuType,
        ConstructiveOverlayType,
        DestructiveOverlayType,
    } from "$lib/types/ui";
    import { browser } from "$app/env";
    import {
        fc,
        task,
        workspaceUser,
        workspace,
        workspaceBoard,
        workspaceBoardSection,
    } from "$lib/storybook";

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

    let contextMenus: ContextMenuType[] = [
        {
            kind: "profile" as const,
        },
        {
            kind: "workspace" as const,
        },
        {
            kind: "sideNav" as const,
            workspace,
        },
        {
            kind: "workspaceBoard" as const,
            workspaceBoard,
        },
        {
            kind: "workspaceBoardSection" as const,
            workspaceBoardSection,
        },
        {
            kind: "task" as const,
            task,
            location: "dashboard",
        },
        {
            kind: "task" as const,
            task,
            location: "task",
        },
        {
            kind: "help",
        },
        {
            kind: "permissions",
        },
    ];

    let constructiveOverlays: ConstructiveOverlayType[] = [
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
    if (browser) {
        setFirstWorkspace();
    }
</script>

{#each destructiveOverlays as target}
    <DestructiveOverlay {target} />
{/each}

{#if browser}
    <div class={fc}>
        {#each contextMenus as target}
            <ContextMenu {target} />
        {/each}
    </div>
{/if}

<div class={fc}>
    {#each constructiveOverlays as target}
        <div class="w-[500px]">
            <ConstructiveOverlay {target} />
        </div>
    {/each}
</div>
