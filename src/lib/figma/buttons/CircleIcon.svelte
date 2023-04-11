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
    import type {
        ButtonAction,
        CircleIconIcon,
        CircleIconSize,
    } from "$lib/figma/types";

    export let size: CircleIconSize;
    export let icon: CircleIconIcon;
    // TODO consider making this optional
    export let disabled: boolean;

    export let action: ButtonAction;

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

<svelte:element
    this={action.kind}
    on:click={action.kind == "button" ? action.action : undefined}
    on:keydown={action.kind == "button" ? action.action : undefined}
    href={action.kind == "a" ? action.href : undefined}
    class={`${sizeMapped} rounded-full border border-transparent text-base-content hover:bg-secondary-hover focus:border-base-content focus:bg-base-100 focus:outline-none active:bg-disabled-background disabled:bg-transparent disabled:text-transparent`}
    class:block={action.kind === "a"}
    {disabled}
>
    <Icon src={iconMapped} style="outline" />
</svelte:element>
