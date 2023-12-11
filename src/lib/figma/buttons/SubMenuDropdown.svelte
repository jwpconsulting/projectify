<script lang="ts">
    import { ChevronDown } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import type { IconSource } from "@steeze-ui/svelte-icon/types";
    import { createEventDispatcher } from "svelte";

    export let label: string;
    export let icon: IconSource;

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    on:click={click}
    class="flex flex-row items-center justify-between px-4 py-3 text-left text-sm font-bold text-base-content hover:bg-secondary-hover focus:bg-base-300 focus:outline-none active:bg-disabled"
>
    <div class="flex flex-row gap-2">
        <Icon src={icon} theme="outline" class="h-4 w-4" />
        <div class="first-letter:uppercase">
            {label}
        </div>
    </div>
    <Icon src={ChevronDown} theme="outline" class="h-4 w-4" />
</button>
