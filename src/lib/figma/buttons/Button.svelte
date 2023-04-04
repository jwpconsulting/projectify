<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { Icon } from "@steeze-ui/svelte-icon";
    import type {
        ButtonStyle,
        ButtonColor,
        ButtonSize,
    } from "$lib/figma/types";

    export let style: ButtonStyle;
    export let color: ButtonColor;
    export let size: ButtonSize;
    export let disabled: boolean;
    export let label: string | null = null;

    $: innerColorStyle = {
        primary: {
            blue: "border-transparent bg-primary text-primary-content group-hover:bg-primary-hover group-active:bg-primary-pressed",
            red: "bg-destructive border-transparent text-destructive-content group-hover:bg-destructive-hover group-active:bg-destructive-pressed",
        },
        secondary: {
            blue: "text-secondary-content border-secondary group-hover:bg-secondary-hover group-hover:text-secondary-content-hover group-hover:border-secondary-content-hover group-active:bg-secondary-pressed group-active:border-border-secondary group-active:text-secondary-content-hover group-focus:bg-transparent group-focus:text-secondary-content",
            red: "text-destructive border-destructive group-hover:bg-destructive-secondary-hover group-hover:text-destructive-hover group-active:bg-destructive-secondary-pressed group-active:text-destructive-pressed group-active:border-destructive",
        },
        tertiary: {
            blue: "text-tertiary-content hover:text-tertiary-content-hover active:text-tertiary-content-hover active:bg-tertiary-pressed focus:text-tertiary-content-hover",
            red: "text-destructive hover:text-destructive-hover active:bg-destructive-secondary-presed active:text-destructive-hover focus:text-destructive-hover",
        },
    }[style.kind][color];
    $: innerSizeStyle = {
        "medium": "text-base",
        "small": "text-sm",
        "extra-small": "text-xs",
    }[size];
    $: iconSizeStyle = {
        "medium": "h-6 w-6",
        "small": "h-5 w-5",
        "extra-small": "h-4 w-4",
    }[size];

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

{#if style.kind === "tertiary"}
    <!-- XXX Not sure if this is the best place to put flex grow here -->
    <button
        on:click={click}
        class={`flex grow flex-row items-center justify-center gap-2 rounded-lg border border-transparent border-transparent px-4 py-2 font-bold focus:outline-none disabled:text-disabled-content ${innerColorStyle} focus:border-border-focus ${innerSizeStyle}`}
        {disabled}
    >
        {#if style.icon && style.icon.position === "left"}
            <Icon
                src={style.icon.icon}
                theme="outline"
                class={iconSizeStyle}
            />
        {/if}
        <slot />
        {#if label}
            {label}
        {/if}
        {#if style.icon && style.icon.position === "right"}
            <Icon
                src={style.icon.icon}
                theme="outline"
                class={iconSizeStyle}
            />
        {/if}
    </button>
{:else}
    <button
        on:click={click}
        class={`group flex grow flex-col items-start gap-2 rounded-llg border border-transparent p-0.5 focus:border-border-focus focus:outline-none`}
        {disabled}
    >
        {#if style.kind === "primary"}
            <div
                class={`flex w-full flex-row items-center justify-center gap-2.5 rounded-lg border px-4  py-2 font-bold group-disabled:bg-disabled group-disabled:text-disabled-primary-content ${innerColorStyle} ${innerSizeStyle}`}
            >
                <slot />
                {#if label}
                    {label}
                {/if}
            </div>
        {:else}
            <div
                class={`flex w-full flex-row items-center justify-center gap-2.5 rounded-lg border px-4  py-2 font-bold group-disabled:border-disabled-content group-disabled:bg-transparent group-disabled:text-disabled-content ${innerColorStyle} ${innerSizeStyle}`}
            >
                <slot />
                {#if label}
                    {label}
                {/if}
            </div>
        {/if}
    </button>
{/if}
