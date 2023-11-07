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
    class="flex w-full flex-row items-center justify-between gap-2 rounded-lg py-2 text-utility hover:text-disabled-primary-content active:text-base-content"
>
    <div class="w-full min-w-max text-left text-3xl font-bold">
        {label}
    </div>
    <Icon
        src={open ? ChevronUp : ChevronDown}
        theme="outline"
        class="h-6 w-6 shrink-0"
    />
</button>
