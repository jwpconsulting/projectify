<script lang="ts">
    import { _ } from "svelte-i18n";
    import IconClose from "./icons/icon-close.svelte";
    import IconSearch from "./icons/icon-search.svelte";
    export let placeholder = $_("search");
    export let searchText = "";
    export let inputElement = null;
</script>

<div class="relative flex grow">
    <input
        bind:this={inputElement}
        type="text"
        {placeholder}
        class="input input-bordered input-sm h-10 grow pl-9"
        bind:value={searchText}
    />
    <div
        class="icon-sm absolute top-0 left-0 flex h-full w-10 items-center justify-center rounded-l-none"
    >
        <IconSearch />
    </div>

    {#if searchText}
        <button
            class="btn btn-ghost btn-square btn-sm absolute right-0 h-full w-10 rounded-l-none"
            on:click={() => (searchText = "")}
        >
            <IconClose />
        </button>
    {/if}
</div>
