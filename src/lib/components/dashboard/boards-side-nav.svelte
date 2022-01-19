<script lang="ts">
    import { Query_DashboardBoardsSideNav } from "$lib/graphql/operations";
    import { query } from "svelte-apollo";
    import AuthGuard from "../authGuard.svelte";

    import { getModal } from "$lib/components/dialogModal.svelte";

    export let selectedWorkspaceUUID;
    export let selectedBoardUUID;

    let res = null;
    let boards = [];

    $: {
        if (selectedWorkspaceUUID) {
            selectedBoardUUID = null;
            res = query(Query_DashboardBoardsSideNav, {
                variables: { uuid: selectedWorkspaceUUID },
            });
        }
    }

    $: {
        if (res && $res.data) {
            boards = $res.data["workspace"]["boards"];

            if (!selectedBoardUUID && boards.length) {
                selectedBoardUUID = boards[0]["uuid"];
            }
        }
    }

    function onAddNewBoard() {
        console.log("Add new Workspace Board");
        getModal("newBoardModal").open();
    }
</script>

<ul class="menu">
    {#if boards}
        {#each boards as board (board.uuid)}
            <li
                class="p-0"
                class:menu-item-active={selectedBoardUUID == board.uuid}
            >
                <a
                    class="h-9 text-xs font-bold capitalize px-8"
                    href="/"
                    on:click|preventDefault={() =>
                        (selectedBoardUUID = board.uuid)}># {board.title}</a
                >
            </li>
        {/each}
        <li class="text-primary">
            <a
                class="h-9 text-xs font-bold capitalize"
                href="/"
                on:click|preventDefault={onAddNewBoard}
                >+ New Workspace Board</a
            >
        </li>
    {/if}
</ul>

<style>
    .menu li > :where(a),
    .menu li > :where(span) {
        @apply px-4 py-0;
    }
    .menu .menu-item-active {
        @apply bg-primary text-base-content;
    }

    .menu .menu-item-active > * {
        @apply text-primary-content;
    }
</style>
