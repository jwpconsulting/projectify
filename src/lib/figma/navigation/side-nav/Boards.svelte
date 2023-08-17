<script lang="ts">
    import { Folder, Plus } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    // import { goto } from "$lib/navigation";
    import Loading from "$lib/components/loading.svelte";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import SelectWorkspaceBoard from "$lib/figma/buttons/SelectWorkspaceBoard.svelte";
    import SideNavMenuCategoryFocus from "$lib/figma/buttons/SideNavMenuCategoryFocus.svelte";
    import { openConstructiveOverlay } from "$lib/stores/globalUi";
    import type { Workspace } from "$lib/types/workspace";

    export let workspace: Workspace;
    let open = true;

    function toggleOpen() {
        open = !open;
    }

    function openCreateWorkspaceBoard() {
        const target = {
            kind: "createWorkspaceBoard" as const,
            workspace,
        };
        const action = {
            kind: "sync" as const,
            action: console.log,
        };
        openConstructiveOverlay(target, action);
    }
</script>

<SideNavMenuCategoryFocus
    label={$_("dashboard.boards")}
    icon={Folder}
    {open}
    on:click={toggleOpen}
    filtered={false}
/>
{#if open}
    <div class="flex flex-col">
        {#if workspace.workspace_boards}
            {#each workspace.workspace_boards as workspaceBoard (workspaceBoard.uuid)}
                <SelectWorkspaceBoard {workspaceBoard} />
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
