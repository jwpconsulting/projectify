<script lang="ts">
    import { Folder, Plus } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    // import { goto } from "$lib/navigation";
    import Loading from "$lib/components/loading.svelte";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import SelectWorkspaceBoard from "$lib/figma/buttons/SelectWorkspaceBoard.svelte";
    import SideNavMenuCategoryFocus from "$lib/figma/buttons/SideNavMenuCategoryFocus.svelte";
    import {
        boardExpandOpen,
        toggleBoardExpandOpen,
    } from "$lib/stores/dashboard";
    import { openConstructiveOverlay } from "$lib/stores/globalUi";
    import type { Workspace } from "$lib/types/workspace";

    export let workspace: Workspace;

    async function openCreateWorkspaceBoard() {
        const target = {
            kind: "createWorkspaceBoard" as const,
            workspace,
        };
        await openConstructiveOverlay(target);
    }
</script>

<SideNavMenuCategoryFocus
    label={$_("dashboard.boards")}
    icon={Folder}
    open={$boardExpandOpen}
    on:click={toggleBoardExpandOpen}
    filtered={false}
/>
{#if $boardExpandOpen}
    <div class="flex flex-col">
        {#if workspace.workspace_boards}
            {#each workspace.workspace_boards as workspaceBoard (workspaceBoard.uuid)}
                <SelectWorkspaceBoard {workspace} {workspaceBoard} />
            {/each}
            <ContextMenuButton
                label={$_("dashboard.create-board")}
                icon={Plus}
                color="primary"
                state="normal"
                kind={{ kind: "button", action: openCreateWorkspaceBoard }}
            />
        {:else}
            <Loading />
        {/if}
    </div>
{/if}
