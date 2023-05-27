<script lang="ts">
    import { _ } from "svelte-i18n";
    // import { goto } from "$app/navigation";
    import { Folder, Plus } from "@steeze-ui/heroicons";
    import Loading from "$lib/components/loading.svelte";
    import SideNavMenuCategoryFocus from "$lib/figma/buttons/SideNavMenuCategoryFocus.svelte";
    import SelectWorkspaceBoard from "$lib/figma/buttons/SelectWorkspaceBoard.svelte";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import { openConstructiveOverlay } from "$lib/stores/globalUi";

    import { currentWorkspace } from "$lib/stores/dashboard";

    let open = true;

    function toggleOpen() {
        open = !open;
    }

    function openCreateWorkspaceBoard() {
        // XXX currentWorkspace is nullable in this context, but Boards
        // should only ever be rendered if currentWorkspace is set... so...
        // Don't make it depend on currentWorkspace from
        // workspaceBoardSearchModule
        if (!$currentWorkspace) {
            throw new Error("Expected $currentWorkspace");
        }
        const target = {
            kind: "createWorkspaceBoard" as const,
            workspace: $currentWorkspace,
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
        {#if $currentWorkspace && $currentWorkspace.workspace_boards}
            {#each $currentWorkspace.workspace_boards as workspaceBoard (workspaceBoard.uuid)}
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
