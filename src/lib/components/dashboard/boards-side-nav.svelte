<script lang="ts">
    import { Mutation_AddWorkspaceBoard } from "$lib/graphql/operations";
    import { client } from "$lib/graphql/client";
    import { getWorkspace } from "$lib/repository";

    import { getModal } from "$lib/components/dialogModal.svelte";
    import { currentWorkspaceLabels } from "$lib/stores/dashboard";
    import { getDashboardWorkspaceBoardUrl } from "$lib/urls";
    import { _ } from "svelte-i18n";
    import type { WorkspaceBoard } from "$lib/types";
    import { currentWorkspace, currentBoardUuid } from "$lib/stores/dashboard";

    let boards: WorkspaceBoard[] = [];

    async function fetchWorkspace() {
        if ($currentWorkspace) {
            $currentWorkspace = await getWorkspace($currentWorkspace.uuid);
        }
    }

    $: {
        if ($currentWorkspace) {
            if ($currentWorkspace.workspace_boards) {
                boards = $currentWorkspace.workspace_boards;
            } else {
                fetchWorkspace();
            }
            if ($currentWorkspace.labels) {
                currentWorkspaceLabels.set([...$currentWorkspace.labels]);
            } else {
                console.debug("Expected workspace.labels");
            }
        }
    }

    async function onAddNewBoard() {
        let modalRes = await getModal("newBoardModal").open();

        if (modalRes?.confirm) {
            try {
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
                $currentBoardUuid = mRes.data.addWorkspaceBoard.uuid;
                // XXX gotoDashboard($currentWorkspaceUuid, $currentBoardUuid);
            } catch (error) {
                console.error(error);
            }
        }
    }
</script>

<ul class="menu block overflow-y-auto">
    {#if boards}
        {#each boards as board (board.uuid)}
            <li
                class="p-0"
                class:menu-item-active={board.uuid === $currentBoardUuid}
            >
                <a
                    class="inline h-9 px-8 text-xs font-bold capitalize"
                    href={getDashboardWorkspaceBoardUrl(board.uuid)}
                    ><span class="nowrap-ellipsis"># {board.title}</span></a
                >
            </li>
        {/each}
        <li
            class="sticky bottom-0 bg-base-100 text-primary hover:text-secondary-content"
        >
            <a
                class="h-9 text-xs font-bold capitalize"
                href="/"
                on:click|preventDefault={onAddNewBoard}
                >+ {$_("new-workspace-board")}</a
            >
        </li>
    {/if}
</ul>

<style>
    .menu li > :where(a),
    .menu li > :where(span) {
        @apply px-4 py-0;
    }
    .menu .menu-item-active > * {
        @apply text-primary-content;
    }
</style>
