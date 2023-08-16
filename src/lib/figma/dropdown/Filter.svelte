<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import { createEventDispatcher } from "svelte";
    import type { IconSource } from "@steeze-ui/svelte-icon/types";
    import { ChevronDown, ChevronUp } from "@steeze-ui/heroicons";

    export let label: string;
    export let icon: IconSource;
    export let open: boolean;

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    on:click={click}
    class="flex max-w-fit flex-row items-center gap-2 rounded-lg border border-border p-2 hover:bg-secondary-hover"
>
    <Icon src={icon} theme="outline" class="h-6 w-6" />
    <div class="truncate text-left text-sm font-bold capitalize">
        {label}
    </div>
    <Icon
        src={open ? ChevronUp : ChevronDown}
        theme="outline"
        class="h-4 w-4"
    />
</button>
