<script lang="ts">
    import { ChevronDown, ChevronUp } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import type { IconSource } from "@steeze-ui/svelte-icon/types";
    import { createEventDispatcher } from "svelte";

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
    class="flex max-w-full flex-row items-center gap-2 overflow-x-hidden rounded-lg border border-border p-2 hover:bg-secondary-hover"
>
    <Icon src={icon} theme="outline" class="h-4 w-4 shrink-0" />
    <div class="min-w-0 shrink truncate text-left text-sm font-bold">
        {label}
    </div>
    <Icon
        src={open ? ChevronUp : ChevronDown}
        theme="outline"
        class="h-4 w-4 shrink-0"
    />
</button>
