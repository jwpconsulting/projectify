<script lang="ts">
    import { _ } from "svelte-i18n";
    import { currentWorkspaceBoardUuid } from "$lib/stores/dashboard";
    import { getModal } from "$lib/components/dialogModal.svelte";
    import { Mutation_AddWorkspaceBoard } from "$lib/graphql/operations";
    import { client } from "$lib/graphql/client";
    // import { goto } from "$app/navigation";
    import Loading from "$lib/components/loading.svelte";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Plus, Folder } from "@steeze-ui/heroicons";
    import SideNavMenuCategoryFocus from "$lib/figma/buttons/SideNavMenuCategoryFocus.svelte";
    import SelectWorkspaceBoard from "$lib/figma/buttons/SelectWorkspaceBoard.svelte";
    import { getDashboardWorkspaceBoardUrl } from "$lib/urls";
    import type { Readable } from "svelte/store";
    import type { Workspace } from "$lib/types/workspace";

    export let currentWorkspace: Readable<Workspace | null>;

    let open = true;

    async function onAddNewBoard() {
        let modalRes = await getModal("newBoardModal").open();

        if (!modalRes?.confirm) {
            console.debug("Expected modalRes.confirm");
            return;
        }
        let mRes = await client.mutate({
            mutation: Mutation_AddWorkspaceBoard,
            variables: {
                input: {
                    workspaceUuid: $currentWorkspace
                        ? $currentWorkspace.uuid
                        : "",
                    title: modalRes.outputs.title,
                    deadline: modalRes.outputs.deadline,
                    description: "",
                },
            },
        });
        $currentWorkspaceBoardUuid = mRes.data.addWorkspaceBoard.uuid;
        if (!$currentWorkspaceBoardUuid) {
            throw new Error("Expected $currentWorkspaceBoardUuid");
        }
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
                <SelectWorkspaceBoard {workspaceBoard} />
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
