<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Search, X } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";
    import type { InputFieldStyle } from "$lib/figma/types";

    export let value = "";
    export let placeholder: string;
    export let style: InputFieldStyle;
    function clear() {
        value = "";
    }
</script>

<div class="relative isolate h-12 w-full p-1">
    <input
        type="text"
        class="text-regular placeholder:text-task-update-text peer relative top-0 left-0 z-10 h-full w-full rounded-lg border border-border pr-8 text-xs placeholder:capitalize focus:outline-none"
        class:pl-2={style !== "search"}
        class:pl-8={style === "search"}
        bind:value
        {placeholder}
    />
    <div
        class="absolute top-0 left-0 z-0 h-full w-full rounded-xl border-2 border-transparent peer-focus:border-border"
    />
    {#if style === "search"}
        <div
            class="absolute top-0.5 left-0.5 z-20 flex flex-row items-center justify-between"
        >
            <div class="flex flex-row gap-2.5 p-3">
                <Icon
                    src={Search}
                    theme="outline"
                    class="h-4 w-4 text-base-content"
                />
            </div>
        </div>
    {/if}
    {#if value}
        <button
            class="absolute right-0.5 top-0.5 z-20 flex flex-row gap-2.5 p-3"
            on:click={clear}
        >
            <Icon src={X} theme="outline" class="h-4 w-4 text-base-content" />
        </button>
    {/if}
</div>
