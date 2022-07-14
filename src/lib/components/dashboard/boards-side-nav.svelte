<script lang="ts">
    import { Mutation_AddWorkspaceBoard } from "$lib/graphql/operations";
    import { client } from "$lib/graphql/client";
    import { getWorkspace } from "$lib/repository";

    import { getModal } from "$lib/components/dialogModal.svelte";
    import {
        gotoDashboard,
        getDashboardURL,
        currentWorkspaceLabels,
    } from "$lib/stores/dashboard";
    import { _ } from "svelte-i18n";
    import { goto } from "$app/navigation";
    import type { WorkspaceBoard, Workspace } from "$lib/types";

    export let selectedWorkspaceUUID: string;
    export let selectedBoardUUID: string | null = null;

    let workspace: Workspace | null = null;
    let boards: WorkspaceBoard[] = [];

    async function fetchWorkspace() {
        workspace = await getWorkspace(selectedWorkspaceUUID);
    }

    $: {
        if (selectedWorkspaceUUID) {
            fetchWorkspace();
        }
    }

    $: {
        if (workspace) {
            if (workspace.workspace_boards) {
                boards = workspace.workspace_boards;
            } else {
                throw new Error("Expected workspace.workspace_boards");
            }
            if (workspace.labels) {
                currentWorkspaceLabels.set([...workspace.labels]);
            } else {
                throw new Error("Expected workspace.labels");
            }

            if (!selectedBoardUUID && boards.length) {
                gotoDashboard(selectedWorkspaceUUID, boards[0]["uuid"]);
            } else {
                const selectedBoard = boards
                    ? boards.find((b) => b.uuid === selectedBoardUUID)
                    : null;

                if (!selectedBoard) {
                    goto("/error/board-not-found");
                }
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
                            workspaceUuid: selectedWorkspaceUUID,
                            title: modalRes.outputs.title,
                            deadline: modalRes.outputs.deadline,
                            description: "",
                        },
                    },
                });
                selectedBoardUUID = mRes.data.addWorkspaceBoard.uuid;
                gotoDashboard(selectedWorkspaceUUID, selectedBoardUUID);
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
                class:menu-item-active={board.uuid === selectedBoardUUID}
            >
                <a
                    class="inline h-9 px-8 text-xs font-bold capitalize"
                    href={getDashboardURL(selectedWorkspaceUUID, board.uuid)}
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
