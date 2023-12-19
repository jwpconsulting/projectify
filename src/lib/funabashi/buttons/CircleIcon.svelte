<script lang="ts">
    import {
        ChevronDown,
        ChevronUp,
        DotsHorizontal,
        Pencil,
        Trash,
        X,
    } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";

    import type {
        ButtonAction,
        CircleIconIcon,
        CircleIconSize,
    } from "$lib/funabashi/types";

    export let size: CircleIconSize;
    export let icon: CircleIconIcon;

    export let action: ButtonAction & { kind: "a" | "button" };

    $: disabled = action.kind === "a" ? false : action.disabled ?? false;

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

    $: styleClasses = `${sizeMapped} rounded-full border border-transparent text-base-content hover:bg-secondary-hover focus:border-base-content focus:bg-base-100 focus:outline-none active:bg-disabled-background`;
</script>

{#if action.kind === "button"}
    <button
        on:click|preventDefault|stopPropagation={action.action}
        {disabled}
        class="{styleClasses} disabled:bg-transparent disabled:text-transparent"
    >
        <Icon src={iconMapped} style="outline" />
    </button>
{:else if action.kind === "a"}
    <a href={action.href} class="block {styleClasses}">
        <Icon src={iconMapped} style="outline" />
    </a>
{/if}
