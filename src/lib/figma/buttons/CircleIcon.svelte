<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import {
        ChevronDown,
        ChevronUp,
        DotsHorizontal,
        Pencil,
        Trash,
        X,
    } from "@steeze-ui/heroicons";
    import { createEventDispatcher } from "svelte";
    import type { CircleIconIcon, CircleIconSize } from "$lib/figma/types";

    export let size: CircleIconSize;
    export let icon: CircleIconIcon;
    // TODO consider making this optional
    export let disabled: boolean;

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }

    $: iconMapped = {
        ellipsis: DotsHorizontal,
        edit: Pencil,
        delete: Trash,
        up: ChevronUp,
        down: ChevronDown,
        close: X,
    }[icon];
    $: sizeMapped = {
        small: "w-6 h-6 p-1",
        medium: "w-8 h-8 p-1.5",
    }[size];
</script>

<button
    on:click|stopPropagation={click}
    class={`${sizeMapped} rounded-full border border-transparent text-base-content hover:bg-secondary-hover focus:border-base-content focus:bg-base-100 focus:outline-none active:bg-disabled-background disabled:bg-transparent disabled:text-transparent`}
    {disabled}
>
    <Icon src={iconMapped} style="outline" />
</button>
