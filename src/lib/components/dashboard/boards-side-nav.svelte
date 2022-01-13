<script lang="ts">
    export let boards = [];
</script>

<ul class="menu">
    {#if boards}
        {#each boards as board}
            <li class="p-0">
                <a class="h-9 text-xs font-bold capitalize px-8" href="/"
                    ># {board.title}</a
                >
            </li>
        {/each}
        <li class="text-primary">
            <a class="h-9 text-xs font-bold capitalize" href="/"
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
</style>
