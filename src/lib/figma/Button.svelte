<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { Icon } from "@steeze-ui/svelte-icon";
    import type {
        ButtonStyle,
        ButtonColor,
        ButtonSize,
        ButtonIcon,
    } from "$lib/figma/types";

    export let style: ButtonStyle;
    export let color: ButtonColor;
    export let size: ButtonSize;
    export let icon: ButtonIcon;
    export let disabled: boolean;

    $: outerColorStyle = {
        primary: {
            blue: "border-transparent focus:border-base-content",
            red: "border-transparent focus:border-base-content",
            black: "border-transparent focus:border-base-content",
        },
        secondary: {
            blue: "border-transparent focus:border-base-content",
            red: "border-transparent focus:border-base-content",
            black: "border-transparent focus:border-base-content",
        },
        tertiary: {
            blue: "border-transparent focus:border-base-content",
            red: "border-transparent focus:border-base-content",
            black: "border-transparent focus:border-base-content",
        },
    }[style][color];
    $: innerColorStyle = {
        primary: {
            blue: "group-disabled:bg-disabled-background group-disabled:text-disabled-text border-transparent bg-primary text-base-100 group-hover:bg-primary-focus group-active:bg-secondary",
            red: "group-disabled:bg-accent bg-accent border-transparent text-accent-content group-hover:bg-accent-focus group-active:bg-accent",
            black: "group-disabled:bg-disabled-background group-disabled:text-disabled-text border-transparent bg-base-content text-base-100 group-hover:bg-secondary-text group-hover:text-base-100 group-active:bg-base-300",
        },
        secondary: {
            blue: "group-disabled:bg-base-100 group-disabled:text-disabled-text group-disabled:border-disabled-text border-primary text-primary group-hover:bg-secondary group-active:bg-secondary-focus group-active:text-primary-content group-focus:bg-primary group-focus:text-primary-content",
            red: "group-disabled:text-accent-content group-disabled:bg-base-100 group-disabled:border-accent-content text-accent-content border-accent-content group-hover:bg-accent group-active:bg-accent-content group-active:text-secondary-content group-active:border-accent group-focus:border-transparent",
            black: "group-disabled:border-disabled-text group-disabled:text-disabled-text group-disabled:bg-base-100 border-base-300 text-base-content group-hover:bg-base-300 group-active:text-base-content group-active:border-base-content group-active:bg-base-100 group-focus:border-transparent group-focus:bg-base-content group-focus:text-base-100",
        },
        tertiary: {
            blue: "disabled:text-primary border-transparent text-primary hover:text-primary-focus focus:border-base-content",
            red: "disabled:text-accent-content border-transparent text-accent-content hover:text-accent-content-hover focus:border-base-content",
            black: "disabled:text-base-content border-transparent text-base-content focus:border-base-content",
        },
    }[style][color];
    $: tertiaryStyle = {
        blue: "hover:bg-secondary",
        red: "",
        black: "hover:bg-base-300",
    }[color];
    $: outerSizeStyle = {
        "medium": "",
        "small": "",
        "extra-small": "",
    }[size];
    $: innerSizeStyle = {
        "medium": "text-base",
        "small": "text-sm",
        "extra-small": "text-xs",
    }[size];

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

{#if style === "tertiary"}
    {#if icon}
        <button
            on:click={click}
            class={`flex flex-row items-center justify-center gap-2 rounded-lg border px-4 py-2 font-bold focus:outline-none ${innerColorStyle} ${innerSizeStyle}`}
            {disabled}
        >
            {#if icon.position === "left"}
                <Icon src={icon.icon} theme="outline" class="h-5 w-5" />
            {/if}
            <slot />
            {#if icon.position === "right"}
                <Icon src={icon.icon} theme="outline" class="h-5 w-5" />
            {/if}
        </button>
    {:else}
        <button
            on:click={click}
            class={`flex flex-row items-center justify-center gap-2 rounded-lg border px-4 py-2 font-bold focus:outline-none ${innerColorStyle} ${innerSizeStyle} ${tertiaryStyle}`}
            {disabled}
        >
            <slot />
        </button>
    {/if}
{:else}
    <button
        on:click={click}
        class={`group flex flex-col items-start gap-2 rounded-llg border p-0.5 focus:outline-none ${outerColorStyle} ${outerSizeStyle}`}
        {disabled}
    >
        <div
            class={`flex flex-row items-center justify-center gap-2.5 rounded-lg border px-4  py-2 font-bold ${innerColorStyle} ${innerSizeStyle}`}
        >
            <slot />
        </div>
    </button>
{/if}
