<script lang="ts">
    import { ChevronDown, ChevronUp } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import type { IconSource } from "@steeze-ui/svelte-icon/types";
    import { createEventDispatcher } from "svelte";

    export let label: string;
    export let icon: IconSource;
    export let filtered: boolean;
    export let open: boolean;
    export let contained: boolean;

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
    let containedStyle: string;
    $: containedStyle = contained
        ? "group-hover:text-base-content"
        : "hover:text-base-content";

    $: outerClass = `flex w-full flex-row justify-between gap-2 px-4 py-2 text-utility ${containedStyle}`;
</script>

<!-- XXX duplication aaaarg -->
{#if contained}
    <div class={outerClass}>
        <div class="flex flex-row items-center gap-4">
            <div class="flex flex-row items-center gap-2">
                <Icon src={icon} theme="outline" class="h-5 w-5" />
                <div class="text-xs font-bold">
                    {label}
                </div>
            </div>
            {#if filtered}
                <div class="h-3 w-3 rounded-full bg-primary" />
            {/if}
        </div>
        <Icon
            src={open ? ChevronUp : ChevronDown}
            theme="outline"
            class="h-4 w-4"
        />
    </div>
{:else}
    <button on:click={click} on:keydown={click} class={outerClass}>
        <div class="flex flex-row items-center gap-4">
            <div class="flex flex-row items-center gap-2">
                <Icon src={icon} theme="outline" class="h-5 w-5" />
                <div class="text-xs font-bold uppercase">
                    {label}
                </div>
            </div>
            {#if filtered}
                <div class="h-3 w-3 rounded-full bg-primary" />
            {/if}
        </div>
        <Icon
            src={open ? ChevronUp : ChevronDown}
            theme="outline"
            class="h-4 w-4"
        />
    </button>
{/if}
