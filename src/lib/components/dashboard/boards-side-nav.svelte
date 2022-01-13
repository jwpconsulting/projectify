<script lang="ts">
    export let boards = [];

    export let selectedBoardUUID;
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
                on:click|preventDefault={() => {}}>+ New Workspace Board</a
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
