<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";

    import type {
        ButtonAction,
        ButtonColor,
        ButtonSize,
        ButtonStyle,
    } from "$lib/funabashi/types";
    import { tw } from "$lib/utils/ui";

    export let style: ButtonStyle;
    export let color: ButtonColor;
    export let size: ButtonSize;
    export let label: string;
    export let action: ButtonAction;
    // XXX Hacky. Buttons have been inserted so far without caring for grow
    // or not. Grow depends on the outside being flex. This means this Button
    // is less "containerized" or "isolated".
    export let grow = true;

    $: innerColorStyle = {
        primary: {
            blue: tw`border-transparent bg-primary text-primary-content group-hover:bg-primary-hover group-active:bg-primary-pressed`,
            red: tw`border-transparent bg-destructive text-destructive-content group-hover:bg-destructive-hover group-active:bg-destructive-pressed`,
        },
        secondary: {
            blue: tw`border-secondary text-secondary-content group-hover:border-secondary-content-hover group-hover:bg-secondary-hover group-hover:text-secondary-content-hover group-active:border-border-secondary group-active:bg-secondary-pressed group-active:text-secondary-content-hover`,
            red: tw`border-destructive text-destructive group-hover:bg-destructive-secondary-hover group-hover:text-destructive-hover group-active:border-destructive group-active:bg-destructive-secondary-pressed group-active:text-destructive-pressed`,
        },
        tertiary: {
            blue: tw`text-tertiary-content hover:text-tertiary-content-hover active:bg-tertiary-pressed active:text-tertiary-content-hover`,
            red: tw`active:bg-destructive-secondary-presed text-destructive hover:text-destructive-hover active:text-destructive-hover`,
        },
    }[style.kind][color];
    $: innerSizeStyle = {
        "medium": tw`text-base`,
        "small": tw`text-sm`,
        "extra-small": tw`text-xs`,
    }[size];
    $: iconSizeStyle = {
        "medium": tw`h-6 w-6`,
        "small": tw`h-5 w-5`,
        "extra-small": tw`h-4 w-4`,
    }[size];

    $: outerStyle = {
        // XXX Not sure if this is the best place to put flex grow here
        primary: tw`group flex ${
            grow ? "grow" : ""
        } flex-col items-start rounded-llg border border-transparent p-0.5 `,
        secondary: tw`? "grow" : ""grow group flex grow flex-col items-start rounded-llg border border-transparent p-0.5 `,
        tertiary: tw`? "grow" : ""grow flex grow flex-row items-center justify-center rounded-lg border border-transparent border-transparent px-4 py-2 font-bold disabled:text-disabled-content ${innerColorStyle} ${innerSizeStyle}`,
    }[style.kind];

    $: innerStyle = {
        primary: tw`flex ${
            grow ? "w-full" : ""
        } flex-row items-center justify-center rounded-lg border px-4 py-2 font-bold group-disabled:bg-disabled group-disabled:text-disabled-primary-content ${innerColorStyle} ${innerSizeStyle}`,
        secondary: tw`flex ${
            grow ? "w-full" : ""
        } flex-row items-center justify-center rounded-lg border px-4 py-2 font-bold group-disabled:bg-disabled group-disabled:text-disabled-primary-content ${innerColorStyle} ${innerSizeStyle}`,
        tertiary: tw`flex ${
            grow ? "w-full" : ""
        } flex-row items-center justify-center rounded-lg border px-4  py-2 font-bold group-disabled:border-disabled-content group-disabled:bg-transparent group-disabled:text-disabled-content ${innerColorStyle} ${innerSizeStyle}`,
    }[style.kind];

    // Outer element properties that button and submit share
    $: formProps =
        action.kind === "button" || action.kind === "submit"
            ? {
                  class: outerStyle,
                  disabled: action.disabled,
                  form: action.form,
              }
            : {};
</script>

{#if style.kind === "tertiary"}
    {#if action.kind === "a"}
        <a href={action.href} class={outerStyle} on:click={action.onInteract}>
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
    {:else if action.kind === "button"}
        <button
            on:click|preventDefault={action.action}
            {...formProps}
            type="button"
        >
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
    {:else}
        Not supported
    {/if}
{:else if action.kind === "a"}
    <a href={action.href} class={outerStyle} on:click={action.onInteract}>
        <div class={innerStyle}>
            {label}
        </div>
    </a>
{:else if action.kind === "button"}
    <button on:click|preventDefault={action.action} {...formProps}>
        <div class={innerStyle}>
            {label}
        </div>
    </button>
{:else}
    <button type="submit" {...formProps}>
        <div class={innerStyle}>
            {label}
        </div>
    </button>
{/if}
