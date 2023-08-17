<script lang="ts">
    import { ChevronDown, ChevronUp } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { createEventDispatcher } from "svelte";

    export let label: string;
    export let open: boolean;

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    on:click={click}
    class="mx-4 flex w-96 flex-row items-center justify-between rounded-lg px-2 py-4 text-utility hover:text-disabled-primary-content focus:outline-none focus:ring-1 focus:ring-border-focus focus:ring-offset-2 active:text-base-content sm:w-72"
>
    <div class="text-3xl font-bold capitalize">
        {label}
    </div>
    <Icon
        src={open ? ChevronUp : ChevronDown}
        theme="outline"
        class="h-6 w-6"
    />
</button>
