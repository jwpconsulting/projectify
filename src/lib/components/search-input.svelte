<script lang="ts">
    import { createEventDispatcher } from "svelte";

    import { _ } from "svelte-i18n";
    import IconClose from "$lib/components/icons/icon-close.svelte";
    import IconSearch from "$lib/components/icons/icon-search.svelte";

    export let placeholder = $_("search");
    export let searchText = "";
    export let inputElement: HTMLElement | null = null;

    export let dispatch = createEventDispatcher();
</script>

<div class="relative flex grow">
    <input
        bind:this={inputElement}
        type="text"
        {placeholder}
        class="input input-bordered input-sm h-10 grow pl-9"
        bind:value={searchText}
        on:blur={() => dispatch("blur")}
    />
    <div
        class="icon-sm absolute top-0 left-0 flex h-full w-10 items-center justify-center rounded-l-none"
    >
        <IconSearch />
    </div>

    {#if searchText}
        <button
            class="btn btn-square btn-ghost btn-sm absolute right-0 h-full w-10 rounded-l-none"
            on:click={() => (searchText = "")}
        >
            <IconClose />
        </button>
    {/if}
</div>
