<script lang="ts">
    import { _ } from "svelte-i18n";

    import IconClose from "../icons/icon-close.svelte";
    import IconSearch from "../icons/icon-search.svelte";

    export let searchText = "";
</script>

<div class="flex grow items-center space-x-4">
    <div class="relative flex grow">
        <input
            type="text"
            placeholder={$_("filter-tasks")}
            class="input input-bordered input-sm grow pl-8"
            bind:value={searchText}
        />
        <div
            class="icon-sm absolute top-0 left-0 flex h-full w-9 items-center justify-center rounded-l-none"
        >
            <IconSearch />
        </div>

        {#if searchText}
            <button
                class="btn btn-ghost btn-square btn-sm absolute right-0 rounded-l-none"
                on:click={() => (searchText = "")}
            >
                <IconClose />
            </button>
        {/if}
    </div>
</div>
