<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Search, X } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    export let searchInput = "";
    export let placeholder: string;
    function clear() {
        searchInput = "";
    }
</script>

<div class="relative p-0.5">
    <input
        type="text"
        class="text-regular placeholder:text-task-update-text h-10 w-full rounded-lg border border-base-300 pl-10 pr-10 text-xs placeholder:capitalize"
        bind:value={searchInput}
        {placeholder}
    />
    <div
        class="absolute top-0.5 left-0.5 flex flex-row items-center justify-between"
    >
        <div class="flex flex-row gap-2.5 p-3">
            <Icon
                src={Search}
                theme="outline"
                class="h-4 w-4 text-base-content"
            />
        </div>
    </div>
    {#if searchInput}
        <button
            class="absolute right-0.5 top-0.5 flex flex-row gap-2.5 p-3"
            on:click={clear}
        >
            <Icon src={X} theme="outline" class="h-4 w-4 text-base-content" />
        </button>
    {/if}
</div>
