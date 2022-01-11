<script lang="ts">
    export let boards = [];
</script>

<main class="bg-wite-1 flex flex-col w-24 items-center p-2">
    {#if boards}
        {#each boards as board}
            <button class="btn btn-primary btn-ghost">{board.title}</button>
        {/each}
    {/if}
</main>

<style lang="scss">
</style>
