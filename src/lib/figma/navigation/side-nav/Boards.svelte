<script lang="ts">
    import { _ } from "svelte-i18n";
    // import { goto } from "$app/navigation";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Folder, Plus } from "@steeze-ui/heroicons";
    import Loading from "$lib/components/loading.svelte";
    import SideNavMenuCategoryFocus from "$lib/figma/buttons/SideNavMenuCategoryFocus.svelte";
    import SelectWorkspaceBoard from "$lib/figma/buttons/SelectWorkspaceBoard.svelte";
    import type { WorkspaceBoardSearchModule } from "$lib/types/stores";

    export let workspaceBoardSearchModule: WorkspaceBoardSearchModule;

    let { currentWorkspace } = workspaceBoardSearchModule;

    let open = true;

    async function onAddNewBoard() {
        // TODO let modalRes = await getModal("newBoardModal").open();
        // TODO if (!modalRes?.confirm) {
        // TODO     console.debug("Expected modalRes.confirm");
        // TODO     return;
        // TODO }
        // TODO let mRes = await client.mutate({
        // TODO     mutation: Mutation_AddWorkspaceBoard,
        // TODO     variables: {
        // TODO         input: {
        // TODO             workspaceUuid: $currentWorkspace
        // TODO                 ? $currentWorkspace.uuid
        // TODO                 : "",
        // TODO             title: modalRes.outputs.title,
        // TODO             deadline: modalRes.outputs.deadline,
        // TODO             description: "",
        // TODO         },
        // TODO     },
        // TODO });
        // TODO $currentWorkspaceBoardUuid = mRes.data.addWorkspaceBoard.uuid;
        // TODO if (!$currentWorkspaceBoardUuid) {
        // TODO     throw new Error("Expected $currentWorkspaceBoardUuid");
        // TODO }
        // TODO
        // goto(getDashboardWorkspaceBoardUrl($currentWorkspaceBoardUuid));
    }

    function toggleOpen() {
        open = !open;
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
                <SelectWorkspaceBoard
                    {workspaceBoardSearchModule}
                    {workspaceBoard}
                />
            {/each}
            <div>
                <button
                    class="flex w-full flex-row gap-2 px-5 py-3 hover:bg-base-200"
                    on:click|preventDefault={onAddNewBoard}
                >
                    <Icon
                        src={Plus}
                        theme="outline"
                        class="h-4 w-4 text-primary"
                    />
                    <div class="text-xs font-bold capitalize text-primary">
                        {$_("dashboard.create-board")}
                    </div>
                </button>
            </div>
        {:else}
            <Loading />
        {/if}
    </div>
{/if}
