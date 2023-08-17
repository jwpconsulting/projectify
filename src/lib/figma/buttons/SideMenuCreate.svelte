<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import type { IconSource } from "@steeze-ui/svelte-icon/types";
    import { createEventDispatcher } from "svelte";

    import type { SideMenuCreateSize } from "$lib/figma/types";

    export let icon: IconSource;
    export let label: string;
    export let size: SideMenuCreateSize;

    let iconClass: string;
    $: iconClass = {
        extraSmall: "w-4 h-4",
        small: "w-5 h-5",
    }[size];

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    on:click={click}
    class="flex flex-row items-center gap-2 border border-transparent px-5 py-3 font-bold text-primary hover:bg-secondary-hover hover:text-primary-hover focus:border-border-focus focus:outline-none active:bg-secondary-pressed active:text-primary-hover"
    class:text-xs={size === "extraSmall"}
    class:text-sm={size === "small"}
>
    <Icon src={icon} theme="outline" class={iconClass} />
    {label}
</button>
