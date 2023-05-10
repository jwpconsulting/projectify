<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { Icon } from "@steeze-ui/svelte-icon";
    import type {
        ButtonAction,
        ButtonColor,
        ButtonSize,
        ButtonStyle,
    } from "$lib/figma/types";

    export let style: ButtonStyle;
    export let color: ButtonColor;
    export let size: ButtonSize;
    export let disabled = false;
    export let label: string;
    export let action: ButtonAction | null = null;

    // TODO refactor to use callback action prop instead

    const dispatch = createEventDispatcher();
    function click() {
        if (action && action.kind == "button") {
            action.action();
            return;
        }
        dispatch("click");
    }

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

    $: outerStyle = {
        // XXX Not sure if this is the best place to put flex grow here
        primary: `group flex grow flex-col items-start gap-2 rounded-llg border border-transparent p-0.5 focus:border-border-focus focus:outline-none`,
        secondary: `group flex grow flex-col items-start gap-2 rounded-llg border border-transparent p-0.5 focus:border-border-focus focus:outline-none`,
        tertiary: `flex grow flex-row items-center justify-center gap-2 rounded-lg border border-transparent border-transparent px-4 py-2 font-bold focus:outline-none disabled:text-disabled-content ${innerColorStyle} focus:border-border-focus ${innerSizeStyle}`,
    }[style.kind];

    $: innerStyle = {
        primary: `flex w-full flex-row items-center justify-center gap-2.5 rounded-lg border px-4 py-2 font-bold group-disabled:bg-disabled group-disabled:text-disabled-primary-content ${innerColorStyle} ${innerSizeStyle}`,
        secondary: `flex w-full flex-row items-center justify-center gap-2.5 rounded-lg border px-4 py-2 font-bold group-disabled:bg-disabled group-disabled:text-disabled-primary-content ${innerColorStyle} ${innerSizeStyle}`,
        tertiary: `flex w-full flex-row items-center justify-center gap-2.5 rounded-lg border px-4  py-2 font-bold group-disabled:border-disabled-content group-disabled:bg-transparent group-disabled:text-disabled-content ${innerColorStyle} ${innerSizeStyle}`,
    }[style.kind];
</script>

{#if style.kind === "tertiary"}
    {#if action && action.kind === "a"}
        <a href={action.href} class={outerStyle}>
            {#if style.icon && style.icon.position === "left"}
                <Icon
                    src={style.icon.icon}
                    theme="outline"
                    class={iconSizeStyle}
                />
            {/if}
            {label}
            {#if style.icon && style.icon.position === "right"}
                <Icon
                    src={style.icon.icon}
                    theme="outline"
                    class={iconSizeStyle}
                />
            {/if}
        </a>
    {:else}
        <button on:click|preventDefault={click} class={outerStyle} {disabled}>
            {#if style.icon && style.icon.position === "left"}
                <Icon
                    src={style.icon.icon}
                    theme="outline"
                    class={iconSizeStyle}
                />
            {/if}
            {label}
            {#if style.icon && style.icon.position === "right"}
                <Icon
                    src={style.icon.icon}
                    theme="outline"
                    class={iconSizeStyle}
                />
            {/if}
        </button>
    {/if}
{:else if action && action.kind === "a"}
    <a href={action.href} class={outerStyle}>
        <div class={innerStyle}>
            {label}
        </div>
    </a>
{:else}
    <button on:click|preventDefault={click} class={outerStyle} {disabled}>
        <div class={innerStyle}>
            {label}
        </div>
    </button>
{/if}
