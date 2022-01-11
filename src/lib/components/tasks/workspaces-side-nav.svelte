<script lang="ts">
    export let workspaces;

    function workspaceIconFrom(title) {
        return title.substr(0, 2);
    }
</script>

<nav class="bg-wite-1 flex flex-col w-24 items-center p-2">
    {#if workspaces}
        {#each workspaces as workspace}
            <button class="btn btn-primary btn-outline"
                >{workspaceIconFrom(workspace.title)}</button
            >
        {/each}
        <button class="btn btn-primary btn-outline">+</button>
    {/if}
</nav>

<style lang="scss">
    nav {
        > * {
            @apply m-2;
        }
    }
    button {
        @apply w-12 h-12;
    }
</style>
