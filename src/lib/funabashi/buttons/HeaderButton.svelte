<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import { createEventDispatcher } from "svelte";
    import { ChevronDown, ChevronUp } from "@steeze-ui/heroicons";
    import type { HeaderButtonType } from "$lib/funabashi/types";

    export let label: string;
    export let type: HeaderButtonType;
    export let open: boolean;

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
        open = !open;
    }
</script>

{#if type == "dropdown"}
    <button
        on:click={click}
        class="active:text:primary flex max-w-fit flex-row items-center gap-2 rounded-lg p-2 text-base-content hover:text-primary focus:outline-none focus:ring-1 focus:ring-border-focus focus:ring-offset-2"
    >
        <div class="text-base font-bold capitalize">
            {label}
        </div>
        <Icon
            src={open ? ChevronUp : ChevronDown}
            theme="outline"
            class="h-4 w-4"
        />
    </button>
{:else}
    <button
        on:click={click}
        class="ptext-base-content flex max-w-fit flex-row items-center gap-2 rounded-lg p-2 hover:text-primary focus:outline-none focus:ring-1 focus:ring-border-focus focus:ring-offset-2 active:text-primary"
    >
        <div class="text-base font-bold capitalize">
            {label}
        </div>
    </button>
{/if}
